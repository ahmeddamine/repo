# AtlasFlow ERP Maroc (MVP)

Prototype SaaS multi-entreprises destiné aux PME marocaines couvrant Comptabilité + Ventes/Achats/Stock.
L’UI est en français, devise MAD (DH), format date JJ/MM/AAAA.

## Démarrage rapide (dev)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

## Structure

* `docs/` : specs, architecture, schéma DB, API, sitemap, plan d’implémentation, stratégie de tests.
* `backend/` : API FastAPI, modèles, moteur d’écritures (posting engine), workflow commercial.
* `tests/` : tests unitaires/integration du moteur d’écritures et des workflows.
