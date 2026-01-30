# Architecture & choix techniques

## Stack
* Front : React + TypeScript (prévu).
* Back : FastAPI (Python) pour rapidité MVP + bonne testabilité.
* DB : PostgreSQL (prod), SQLite pour dev/tests rapides.
* Jobs async : Redis + worker (PDF, imports, emails).
* Stockage : S3 compatible.
* Reporting : exports PDF/Excel.

## Schéma textuel
```
UI Web (React)
  -> API Gateway (FastAPI)
      -> Service Comptabilité (posting engine)
      -> Service Commercial (devis/commandes/livraisons)
      -> Service Stock (CMUP)
      -> Service TVA
      -> Service Banque (imports/rapprochements)
      -> Service Documents (S3 + versioning)
      -> Audit & RBAC
  -> PostgreSQL (multi-tenant)
  -> Redis Queue (PDF, emails, imports)
  -> S3 (pièces)
```

## E-invoicing ready (2026)
* Adaptateurs : `connectors/` (DGI, tiers privés).
* Signature : service dédié (HSM/PKI).
* Archivage : coffre-fort S3 + hash + horodatage.
* Traçabilité : AuditEvent + journal immuable.
