# © 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project Stage Use Timesheets",
    "version": "12.0.1.0.0",
    "summary": "Defaults the Use Timesheets field depending on the stage of "
    "the project/analytic account",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "category": "Generic",
    "depends": ["project_wbs_stage", "hr_timesheet"],
    "license": "AGPL-3",
    "data": ["views/analytic_account_stage_view.xml"],
    "installable": True,
}
