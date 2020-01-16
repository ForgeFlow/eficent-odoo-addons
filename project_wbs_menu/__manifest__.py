# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project WBS menus",
    "version": "12.0.1.0.0",
    "author": "ForgeFlow S.L.",
    "category": "Project",
    "summary": "Separate menus for WBS components",
    "website": "http://www.forgeflow.com/",
    "license": "AGPL-3",
    "depends": [
        "project_wbs_stage",
        "project_progress_measurement",
    ],
    "data": [
        "views/project_view.xml",
    ],
    'installable': True,
}
