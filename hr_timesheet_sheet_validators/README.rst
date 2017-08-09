.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
HR Timesheet Sheet Validators
=============================

This module allows a user outside of the Human Resources groups to validate
timesheets. A rule is predefined, but it is flexible enough to accept
extensions.

Timesheets in Odoo can be validated by users belonging to the group
“Human Resources / Officer”. However it is frequent for companies allow to
employees outside of the Human Resources group to validate timesheet.

At the time when a user submits a timesheet to the Manager, the application
determines the validators.

Only those validators or employees in the group of Human Resources Officer
are capable of approving the timesheet.

The current rule sets as validators of a timesheet:

* The head of the department that the employee belongs to

- In case that the employee is head of the department, it will attempt to add
  the head of the parent department instead.

* The employee’s direct manager

The list of validators is visible in the employee’s timesheet.

Usage
=====

To use this module:

#. Go to 'Timesheets > Time Tracking > Timesheets to Approve'
#. Enter a timesheet to approve and click 'Approve'. The new rules will be
   appliying.
#. Also, you can check extra validators in the tab 'Validators' of any
   timesheet.

Credits
=======

Contributors
------------

* Jordi Ballester <jordi.ballester@eficent.com>
* Lois Rilo <lois.rilo@eficent.com>
* Serpent Consulting Services Pvt. Ltd. <support@serpentcs.com>
