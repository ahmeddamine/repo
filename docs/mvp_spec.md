# Spécification MVP (Maroc)

## Périmètre MVP exact

### Obligations Maroc intégrées
* Langue UI : Français, devise MAD (DH), format date JJ/MM/AAAA.
* TVA : taux normal 20% + taux réduits 14%, 10%, 7% configurables.
* Factures : mentions obligatoires (IF, ICE, identité, adresses, date, détail, TVA, total, modalités).
* Piste d’audit : journal “qui a fait quoi, quand, avant/après”.
* Facturation électronique : architecture “e-invoicing ready” (connecteurs, signature, archivage, traçabilité).
* Délais de paiement : échéances, relances/pénalités configurables, reporting “retards”.

### Modules MVP
* Comptabilité : plan comptable, journaux, périodes fiscales, clôture + verrouillage, grand livre, balance, lettrage, TVA simple.
* Commercial : devis → commande → livraison → facture → encaissement, achats, stock CMUP.
* Banque : import CSV/OFX, rapprochement, anomalies.
* Pièces : stockage sécurisé, historisation, anti-suppression.
* Reporting : ventes, TVA, impayés, trésorerie, stock.

### Livrables MVP
* API + moteur d’écritures (posting engine).
* Auth + gestion des tiers (clients/fournisseurs).
* Articles/services + stock (CMUP).
* Workflow complet client (devis → commande → livraison → facture → encaissement).
* Exports PDF/Excel.

### Méthode de valorisation stock (MVP)
* CMUP (coût moyen unitaire pondéré) :
  * Nouveau coût moyen = (stock actuel * coût moyen actuel + quantité reçue * coût achat) / nouveau stock.

## Backlog V1 (extraits)
* Stock multi-dépôts + emplacements.
* TVA avancée (exonérations, prorata, déclarations détaillées).
* Facturation électronique officielle (connecteurs, signature qualifiée).
* Workflows d’achats avancés + retours.
* Reportings personnalisables, BI.
