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

from openerp.osv import orm, fields


class MailNotification(orm.Model):
    _inherit = 'mail.notification'

    def get_partners_to_notify(self, cr, uid, message, partners_to_notify=None, context=None):

        res = super(MailNotification, self).get_partners_to_notify(
            cr, uid, message, partners_to_notify=partners_to_notify,
            context=context)

        for notification in message.notification_ids:
            if notification.read:
                continue
            partner = notification.partner_id
            # If partners_to_notify specified: restrict to them
            if partners_to_notify is not None and \
                    partner.id not in partners_to_notify:
                continue
            # Do not send to partners without email address defined
            if not partner.email:
                continue
            # Do not send emails to partners that have their own fetchmail,
            # and the fetchmail is confirmed.
            if (
                partner.notification_email_send != 'none' and
                message.type == 'email' and
                partner.fetchmail_server_id and
                partner.fetchmail_server_id.state == 'done'
            ):
                if partner.id in res:
                    res.remove(partner.id)
                else:
                    continue
        return res
