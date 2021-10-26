# Copyright 2021 ForgeFlow Sl.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import time
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import ValidationError


class AccountAnalyticJournal(models.Model):
    _name = 'account.analytic.journal'

    restrict_future_entries_posted = fields.Boolean(
        string="Restrict posting analytic entries in the future")
