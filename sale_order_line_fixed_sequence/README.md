Sale order lines with fixed sequence
====================================

Prevent unwanted reordering of sale order lines
-----------------------------------------------

Odoo sets the sequence number on every new sale order line to 10. So when you save the sale order for the first time the order of your lines is not fixed.
This module changes this behaviour while allocating the next free number to every new position.
