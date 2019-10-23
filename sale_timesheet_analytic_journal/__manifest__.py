# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale timesheet analytic journal",
    "version": "12.0.1.0.0",
    "author": "Eficent",
    "category": "HR",
    "summary": """Analytic journal for timesheets""",
    "website": "http://www.eficent.com/",
    "license": "AGPL-3",
    "depends": ["sale_timesheet", "analytic_cost_revenue", "analytic_journal"],
    "data": ["demo/analytic_journal_data.xml"],
    "installable": True,
    "auto_install": True,
}
