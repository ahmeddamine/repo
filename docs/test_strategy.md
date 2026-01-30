# Stratégie de tests

## Unitaires
* Moteur d’écritures : équilibre débit/crédit.
* Stock CMUP : recalcul coût moyen.

## Intégration (workflows)
1. Client → devis → commande → livraison → facture → encaissement → écritures.
2. Fournisseur → BC → réception → facture → paiement → écritures.
3. Import relevé → rapprochement → anomalies.
4. Clôture période → verrouillage + exceptions admin.

## Performance & observabilité
* Pagination, indexation, recherche.
* Logs structurés, métriques, alertes.
