# Copyright 2021 FrgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project WBS Cost Risk",
    "version": "10.0.1.1.0",
    "summary": "Cost Risk in WBS deliverables based on timesheets",
    "author": "ForgeFlow",
    "license": "AGPL-3",
    "website": "http://www.forgeflow.com",
    "category": "Project",
    "depends": ["project_wbs", "hr_timesheet_sheet", "web_tree_dynamic_colored_field", "analytic_cost_revenue"],
    "data": [
        "data/ir_cron.xml",
        "views/account_analytic_account_view.xml",
        "views/project_project_view.xml",        
    ],
    'post_init_hook': 'post_init_hook',
    "installable": True,
}
