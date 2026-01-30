# Plan d’implémentation (sprints)

## Sprint 1 (MVP coeur)
* Modèle multi-tenant + auth + RBAC.
* CRUD tiers + articles + TVA.
* Workflow ventes complet (devis → commande → livraison → facture → encaissement).
* Posting engine (AR, TVA, stock CMUP).

## Sprint 2
* Achats (BC → réception → facture → paiement) + posting.
* Banque : import CSV/OFX, rapprochement.
* Pièces jointes + audit trail.

## Sprint 3
* TVA avancée, clôture période.
* Reporting exports PDF/Excel.
* Optimisations perf + observabilité.
