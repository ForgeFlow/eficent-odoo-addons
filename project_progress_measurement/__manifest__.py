# Copyright 2014-17 ForgeFlow S.L.
#        <contact@forgeflow.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Project progress measurement",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)," "Project Expert Team",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Project Management",
    "license": "AGPL-3",
    "depends": ["project", "progress_measurement", "project_wbs"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/progress_measurements_entry_view.xml",
        "wizard/progress_measurement_quick_entry_view.xml",
        "views/project_progress_measurement_view.xml",
        "views/project_project_view.xml",
    ],
    "installable": True,
    "application": True,
}
