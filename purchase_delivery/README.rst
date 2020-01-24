.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================
Purchase Delivery Costs
=======================

Allows you to add delivery methods in purchase orders and picking.

This module makes it possible to add delivery method to purchase orders and
can compute a shipping line in the purchase order or in the invoice when
created from an incoming shipment.

The application makes use of the same concepts of carrier and delivery grid
extending them as follows:
* Introduces origin countries, states and ZIP in the delivery grid.

* Uses the cost defined in the grid, instead of the sale price.

* Uses the vendor address to match with the existing grid based on the
  origin information defined in the grid.

* Uses the destination address (customer address for direct shipments
  and warehouse otherwise) to determine the grid, based on the destination
  parameters defined in the grid.

In case that the incoming shipment contains moves that have multiple
destination addresses, computes the average freight cost.

Credits
=======

Contributors
------------

* Eficent <http://www.eficent.com>
* Serpent Consulting Services Pvt. Ltd. <support@serpentcs.com>
