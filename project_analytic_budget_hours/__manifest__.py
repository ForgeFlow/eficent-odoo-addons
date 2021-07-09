# Copyright 2020 FrgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project Budget Hours",
    "version": "10.0.1.0.0",
    "summary": "Set budget hours in project and deliverables",
    "author": "Eficent",
    "license": "AGPL-3",
    "website": "http://www.forgeflow.com",
    "category": "Project",
    "depends": ["project_wbs", "hr_timesheet_sheet"],
    "data": [
        "views/account_analytic_account_view.xml",
        "views/project_project_view.xml",
    ],
    "installable": True,
}
