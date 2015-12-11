# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import datetime
import logging
import time
import re
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from openerp.osv import fields, orm
from openerp import tools

_logger = logging.getLogger(__name__)


class FetchMailServer(orm.Model):
    _inherit = 'fetchmail.server'

    _columns = {
        'imap_fetch_from_last_date': fields.boolean(
            'Fetch from last fetch date',
            help='Fetch only IMAP emails that have not yet been received from '
                 'the last check.'),
        'mailbox_ids': fields.one2many(
            'fetchmail.server.mailbox', 'server_id', 'Mailboxes'),
        'mailbox_path_ids': fields.one2many(
            'fetchmail.server.mailbox.path', 'server_id', 'Mailbox paths',
            readonly=True),

    }

    def fetch_mail(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        context['fetchmail_cron_running'] = True
        mail_thread = self.pool.get('mail.thread')
        action_pool = self.pool.get('ir.actions.server')
        check_original = []

        for server in self.browse(cr, uid, ids, context=context):
            if not server.imap_fetch_from_last_date or server.type == 'pop':
                check_original.append(server.id)
                continue

            _logger.info('start checking for new emails on %s server %s',
                         server.type, server.name)
            context.update({'fetchmail_server_id': server.id,
                            'server_type': server.type})
            count, failed = 0, 0
            imap_server = False
            fetch_date = datetime.strptime(server.date,
                                           "%Y-%m-%d %H:%M:%S").date()
            fetch_date = fetch_date.strftime("%d-%b-%Y")
            if server.type == 'imap':
                try:
                    imap_server = server.connect()
                    for mailbox in server.mailbox_ids:
                        if imap_server.select(mailbox.path)[0] != 'OK':
                            _logger.error('Could not open mailbox %s on %s',
                                          mailbox.path, server.name)
                            imap_server.select()
                            continue
                        imap_server.select(mailbox.path)
                        result, data = imap_server.search(
                            None, '(SINCE {date})'.format(date=fetch_date))
                        for message_uid in data[0].split():
                            res_id = None
                            result, data = imap_server.fetch(message_uid,
                                                             '(RFC822)')
                            try:
                                res_id = mail_thread.message_process(
                                    cr, uid, server.object_id.model,
                                    data[0][1],
                                    save_original=server.original,
                                    strip_attachments=(not server.attach),
                                    context=context)
                            except Exception:
                                _logger.exception('Failed to process mail '
                                                  'from %s server %s.',
                                                  server.type, server.name)
                                failed += 1
                            if res_id and server.action_id:
                                action_pool.run(cr, uid, [server.action_id.id],
                                                {'active_id': res_id,
                                                 'active_ids': [res_id],
                                                 'active_model': context.get(
                                                     "thread_model",
                                                     server.object_id.model)})
                            cr.commit()
                            count += 1
                        _logger.info("Fetched %d email(s) on %s server %s; "
                                     "and mailbox %s. %d succeeded, "
                                     "%d failed.",
                                     count, server.type,
                                     server.name, mailbox.path,
                                     (count - failed), failed)
                except Exception:
                    _logger.exception("General failure when trying to "
                                      "fetch mail from %s server %s.",
                                      server.type, server.name)
                finally:
                    if imap_server:
                        imap_server.close()
                        imap_server.logout()
            server.write({'date': time.strftime(
                tools.DEFAULT_SERVER_DATETIME_FORMAT)})
        return super(FetchMailServer, self).fetch_mail(
            cr, uid, check_original, context)

    def _parse_list_response(self, cr, uid, line, context=None):
        list_response_pattern = re.compile(
            r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
        match = list_response_pattern.match(line)
        flags, delimiter, mailbox_name = match.groups()
        mailbox_name = mailbox_name.strip('"')
        return (flags, delimiter, mailbox_name)

    def list_mailboxes(self, cr, uid, ids, context=None):
        mailbox_obj = self.pool['fetchmail.server.mailbox']

        for server in self.browse(cr, uid, ids, context=context):
            mailbox_ids = [m.id for m in server.mailbox_ids]
            mailbox_obj.unlink(cr, uid, mailbox_ids, context=context)
            try:
                imap_server = server.connect()
                typ, data = imap_server.list()
                for line in data:
                    flags, delimiter, mailbox_name = \
                        self._parse_list_response(cr, uid, line,
                                                  context=context)
                    mailbox_obj.create(cr, uid, {'server_id': server.id,
                                                 'path': mailbox_name},
                                       context=context)
            except Exception:
                _logger.exception("General failure when trying to "
                                  "fetch mail from %s server %s.",
                                  server.type, server.name)
        return True
