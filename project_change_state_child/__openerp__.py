# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Project change state child",
    "version": "1.0", 
    "author": "Eficent",
    "category": "Generic Modules/Projects & Services",
    "description": """
Project Change state child
======================================
When a project is set to 'Closed' state:
* All the child projects are also set to status 'Cancelled'
* All child tasks in the hierarchy that were not in status
'Cancelled' or 'Closed' are now set to status 'Closed' and
to a stage associated with this status.


When a project is set to 'Cancelled' state:
* All the child projects are also set to status 'Cancelled'
* All child tasks in the hierarchy that were not in status
'Cancelled' or 'Closed' are now set to status 'Cancelled'
and to a stage associated with this status.

When a project is set to 'Pending' state:
* All the child projects are also set to status 'Pending'
* All child tasks in the hierarchy that were not in status
'Cancelled' or 'Closed' are now set to the stage associated
to the status 'Pending' and to a stage associated with this
status.

When a project is set to 'Open' state:
* All the child projects are also set to status 'Open'
* All child tasks in the hierarchy that were in status
'Cancelled' or 'Closed' are now set to status 'Open' and
to a stage associated with this status.


""", 
    "website": "http://www.eficent.com/",
    "license": "", 
    "depends": [
        "project",
    ], 
    "demo": [], 
    "data": [],
    "test": [], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 
    "auto_install": False, 
    "active": False
}