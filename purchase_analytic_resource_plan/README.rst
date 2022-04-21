.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License AGPL-3

========================================
Purchase for Projects - Create resources
========================================

When receiving a purchase order for a project:
* If the purchase order line is linked to a resource plan line then the system does nothing
* If the purchase order line is not linked to a resource plan line the system:
    * If there is a resource plan line for the same project and the same product and not
           linked to any other purchase order then the system will update that resource
           plan line with the new quantity
    * In any other case the system will create a new resource plan line

Credits
=======

Contributors
------------

* Aaron Henriquez <aaron.henriquez@forgeflow.com>
