# -*- coding: utf-8 -*-
# © 2014 Alexis de Lattre <alexis.delattre@akretion.com>
# © 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
from openerp.tools import email_split
from openerp.exceptions import Warning
import requests
import tempfile
import StringIO
import zipfile
import os
import logging

try:
    import unicodecsv
except ImportError:
    unicodecsv = None

logger = logging.getLogger(__name__)


class BetterZipGeonamesImport(orm.TransientModel):
    _name = 'better.zip.geonames.import'
    _description = 'Import Better Zip from Geonames'
    _rec_name = 'country_id'

    _columns={
        'country_id': fields.many2one('res.country', 'Country', required=True),
        'title_case': fields.boolean(
            string='Title Case',
            help='Converts retreived city and state names to Title Case.',
        )
    }
    def transform_city_name(self, cr, uid, city, country, context=None):
        """Override it for transforming city name (if needed)
        :param city: Original city name
        :param country: Country record
        :return: Transformed city name
        """
        return city

    def _domain_search_better_zip(self, cr, uid, row, country, context=None):
        return [('name', '=', row[1]),
                ('city', '=', self.transform_city_name(cr,
                                                       uid, row[2], country)),
                ('country_id', '=', country.id)]

    def _prepare_better_zip(self, cr, uid, row, country, context=None):
        state = self.select_or_create_state(cr, uid,
                                            row = row,
                                            country = country,
                                            code_row_index=4,
                                            name_row_index=3,
                                            context = context)
        vals = {
            'name': row[1],
            'city': self.transform_city_name(cr, uid, row[2], country),
            'state_id': state,
            'country_id': country.id,
            }
        return vals

    def create_better_zip(self, cr, uid, row, country, title_case,
                          context=None):
        if row[0] != country.code:
            raise Warning(
                _("The country code inside the file (%s) doesn't "
                    "correspond to the selected country (%s).")
                % (row[0], country.code))
        logger.debug('ZIP = %s - City = %s' % (row[1], row[2]))
        if (title_case):
            row[2] = row[2].title()
            row[3] = row[3].title()
        if row[1] and row[2]:
            zip_model = self.pool.get('res.better.zip')
            zips = zip_model.search(cr, uid,
                                    self._domain_search_better_zip(cr, uid,
                                    row, country))
            if zips:
                return zips[0]
            else:
                vals = self._prepare_better_zip(cr,uid, row, country)
                if vals:
                    return zip_model.create(cr, uid, vals)
        else:
            return False

    def select_or_create_state(
            self, cr, uid, row, country, code_row_index=4, name_row_index=3,
            context=None):
        states = self.pool.get('res.country.state').search(cr,uid,[
            ('country_id', '=', country.id),
            ('code', '=', row[code_row_index]),
            ])
        if len(states) > 1:
            raise Warning(
                _("Too many states with code %s for country %s")
                % (row[code_row_index], country.code))
        if len(states) == 1:
            return states[0]
        else:
            return self.pool.get('res.country.state').create(cr,uid,{
                'name': row[name_row_index],
                'code': row[code_row_index],
                'country_id': country.id
                })

    def run_import(self, cr, uid, fields, context=None):
        zip_model = self.pool.get('res.better.zip')
        data = self.browse(cr, uid, fields, context=context)[0]
        title_case = data.title_case
        country_code = data.country_id.code
        country = data.country_id
        country_id = data.country_id.id
        country_name = data.country_id.name
        config_url = self.pool.get('ir.config_parameter').get_param(cr,uid,
            'geonames.url',
            default='http://download.geonames.org/export/zip/%s.zip')
        url = config_url % country_code
        logger.info('Starting to download %s' % url)
        res_request = requests.get(url)
        if res_request.status_code != requests.codes.ok:
            raise UserError(
                _('Got an error %d when trying to download the file %s.')
                % (res_request.status_code, url))
        # Store current record list
        zips_to_delete = zip_model.search(cr,uid,
            [('country_id', '=', country_id)])
        f_geonames = zipfile.ZipFile(StringIO.StringIO(res_request.content))
        tempdir = tempfile.mkdtemp(prefix='openerp')
        f_geonames.extract('%s.txt' % country_code, tempdir)
        logger.info('The geonames zipfile has been decompressed')
        data_file = open(os.path.join(tempdir, '%s.txt' % country_code), 'r')
        data_file.seek(0)
        logger.info('Starting to create the better zip entries')
        max_import = context.get('max_import', 0)
        reader = unicodecsv.reader(data_file, encoding='utf-8', delimiter='	')
        for i, row in enumerate(reader):
            zip_code = self.create_better_zip(cr,uid,row, country, title_case,
                                              context)
            if zip_code in zips_to_delete:
                zips_to_delete -= zip_code
            if max_import and i == max_import:
                break
        data_file.close()
        if zips_to_delete and not max_import:
            zips_to_delete.unlink()
            logger.info('%d better zip entries deleted for country %s' %
                        (len(zips_to_delete), country_name))
        logger.info(
            'The wizard to create better zip entries from geonames '
            'has been successfully completed.')
        return True
