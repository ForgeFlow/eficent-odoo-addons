# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project Percent Completed",
    "version": "10.0.1.0.0",
    "summary": """Calculates the % completed on a project, based on the
        duration of the project and the progress measurement.""",
    "category": "Generic Modules/Projects & Services",
    "author": "Eficent",
    "website": "www.eficent.com",
    "license": "AGPL-3",
    "depends": [
        "analytic",
        "project_progress_measurement",
        "project_wbs"
    ],
    "data": [
        "view/project_view.xml"
    ],
    "installable": True,
    "application": True,
}
