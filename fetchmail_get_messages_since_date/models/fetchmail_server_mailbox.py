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
from openerp.osv import fields
from openerp.osv.orm import Model


class FetchMailServerMailbox(Model):
    _name = 'fetchmail.server.mailbox'
    _rec_name = 'path'

    _columns = {
        'path': fields.char(
            'Path', size=256, help='The path to your mail '
            "folder. Typically would be something like 'INBOX.myfolder'",
            required=True
        ),
        'server_id': fields.many2one('fetchmail.server', 'Server'),
    }
