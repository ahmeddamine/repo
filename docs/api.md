# API (extraits)

## Auth
* `POST /auth/login`
* `POST /auth/refresh`

## Tiers
* `POST /clients`
* `POST /suppliers`
* `GET /clients?search=`

## Articles
* `POST /items`
* `GET /items?search=`

## Workflow ventes
* `POST /quotes`
* `POST /quotes/{id}/confirm`
* `POST /deliveries`
* `POST /invoices`
* `POST /payments`

## Comptabilité
* `GET /ledger`
* `GET /trial-balance`
* `POST /periods/close`
