# Copyright 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.change_management.tests.test_changes import TestChanges


class TestChangeManagementOwnProject(TestChanges):

    @classmethod
    def setUpClass(cls):
        super(TestChangeManagementOwnProject, cls).setUpClass()

    def test_change_project(self):
        self.test_change_id.button_create_change_project()
        ch_project = self.test_change_id.change_project_id
        self.assertEqual(
            ch_project.parent_id,
            self.test_project_id.analytic_account_id, "Bad parent project")
