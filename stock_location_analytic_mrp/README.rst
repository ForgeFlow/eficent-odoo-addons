===========================
Stock Location Analytic MRP
===========================

MRP project locations

If the analytic_account_id of the locations does not match with the analytic_account_id
of the mrp.production, then it raises a validation error.

When the analytic_account_id field is modified. It sets the analytic_account_id of all
the raw material moves and finished product moves related to the mrp.production record 

Credits
=======

Contributors
------------

* Aaron Henriquez <aaron.henriquez@forgeflow.com>
