.. image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL-3

======================
Stock Analytic Reserve
======================

This module allows you to reserve / unreserve stock for a specific Analytic
Account / Project.


Configuration
=============


* Go to *Warehouse / Configuration / Warehouses* and
  define, for each warehouse, a Stock Analytic Reservation Location.

* The Stock Analytic Reservation Location must be of 'Location Type' =
  'Inventory'

* If you handle real time inventory valuation then must have as Stock
  Valuation Accounts (Incoming and Outgoing) the same GL account, and must
  be of type 'Asset'.


Usage
=====

* Go to *Inventory / Inventory Control / Stock Analytic Reservation*
  and create a new entry.

* If you select the reservation action 'Reserve', the product entered will
  be reserved to the analytic account indicated.

* If you select the reservation action 'Unreserve', the product entered will
  be unreserved from the analytic account indicated.

* Press 'Prepare' to create the stock moves associated to each line.

* Press 'Confirm' to confirm the stock moves. If some of the products that
  have been requested to be reserved/unreserved are not available, you will
  see in each line, in field 'Out Move Status', the value 'Waiting
  Availability'.

* Press 'Check Availability' to check again the availability of products for
  the selected stock location. Press 'Force Availability' to force the
  products to be withdrawn from the selected location, even when no stock is
  available.

* Press 'Complete' to complete the operation. The products will then be
  reserved/unreserved to/from the selected analytic account.


Credits
=======

Contributors
------------

* Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
