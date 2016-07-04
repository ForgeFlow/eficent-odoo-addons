.. image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL-3

===================
Timesheet approvers
===================

It is frequent for companies to restrict the visibility of
timesheets only to certain employees.

The current functionality allows any user in groups:
* 'Human Resources / Officer'
* 'Human Resources / Manager'

, to list and approve any timesheet.

This module adds the following features:

* Adds an additional layer of security for users in group 'Human Resources
  Officer', to allow only to approve timesheets to the manager of the
  department to which the employee is assigned,
  or to the employee's manager.

* Adds a default filter on timesheets to approve "Mine to Approve", that will
  show only  the timesheets that are associated to the department's or
  employee manager. As a consequence, even users in group 'Human Resources /
  Manager' will know which timesheets they should approve.

* Adds the deparment and employee's manager to the timesheet form and list
  views. Shows the department of the employee, in the form and tree views.

* When the timesheet is confirmed, the manager of the department is added as
  a follower.


Credits
=======

Contributors
------------

* Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
