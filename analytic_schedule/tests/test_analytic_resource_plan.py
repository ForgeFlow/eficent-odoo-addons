# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TestAnalyticSchedule(common.SavepointCase):
    def setUp(cls):
        super(TestAnalyticSchedule, cls).setUp()
        cls.project_project = cls.env["project.project"]

        cls.project = cls.project_project.create(
            {"name": "Test project", "code": "AS0001"}
        )
        cls.parent_account = cls.project.analytic_account_id
        cls.project_son = cls.project_project.create(
            {"name": "Test project son", "code": "AS01"}
        )
        cls.son_account = cls.project_son.analytic_account_id
        cls.son_account.parent_id = cls.parent_account
        cls.project_grand_son = cls.project_project.create(
            {"name": "Test project grand son", "code": "AS01/01"}
        )
        cls.grand_son_account = cls.project_grand_son.analytic_account_id
        cls.grand_son_account.parent_id = cls.son_account

    def test_schedule(cls):
        date = datetime.strftime(datetime.today(), DEFAULT_SERVER_DATE_FORMAT)
        cls.project_grand_son.date_start = date
        cls.project_grand_son.date = date

        cls.assertEquals(
            cls.parent_account.date_start, cls.grand_son_account.date_start
        )
        cls.project_son.date = datetime.strftime(
            datetime.today() + relativedelta(months=9),
            DEFAULT_SERVER_DATE_FORMAT,
        )
        cls.assertNotEqual(
            cls.grand_son_account.date,
            cls.son_account.date,
            "Should Not propagate downwards",
        )
        cls.assertEquals(
            cls.son_account.date,
            cls.parent_account.date,
            "Should propagate upwards",
        )
