from datetime import datetime

from odoo.tests import common


class TestProjectProject(common.TransactionCase):
    def test_compute_scheduled_dates(self):
        project1 = self.env["project.project"].create({"name": "Project 1"})
        project2 = self.env["project.project"].create(
            {"name": "Project 2", "date_start": "2022-01-01", "date": "2022-01-31"}
        )
        project3 = self.env["project.project"].create(
            {"name": "Project 3", "date_start": "2022-02-01", "date": "2022-02-28"}
        )
        aa1 = self.env["account.analytic.account"].create(
            {
                "name": "Analytic Account 1",
                "child_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Child 1",
                            "project_ids": [(4, project2.id), (4, project3.id)],
                        },
                    )
                ],
            }
        )
        project1.write({"analytic_account_id": aa1.id})
        project1._compute_scheduled_dates()
        self.assertEqual(
            datetime.strftime(project1.date_start, "%Y-%m-%d"),
            "2022-01-01",
            "Project start date is not the earliest child start date",
        )
        self.assertEqual(
            datetime.strftime(project1.date, "%Y-%m-%d"),
            "2022-02-28",
            "Project end date is not the latest child end date",
        )
