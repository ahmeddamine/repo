# Schéma DB (minimum)

## Tables principales
* tenants, users, roles_permissions
* clients, suppliers, contacts
* items, warehouses, stock_movements
* quotes, sales_orders, deliveries, invoices, credit_notes
* purchase_orders, receipts, supplier_invoices, payments
* accounts, journals, journal_entries, journal_lines
* tax_rates, tax_profiles
* attachments, audit_events

## Index clés
* `tenant_id` sur toutes les tables.
* `number`, `date`, `status` sur pièces (devis/factures/BL/BC).
* `client_id`, `supplier_id`, `item_id`.
* `journal_entries.date`, `journal_lines.account`.
