from decimal import Decimal

from sqlalchemy.orm import Session

from app import models


def create_entry(session: Session, tenant_id: int, reference: str, date, description: str):
    entry = models.JournalEntry(
        tenant_id=tenant_id,
        reference=reference,
        date=date,
        description=description,
    )
    session.add(entry)
    return entry


def add_line(entry: models.JournalEntry, account: str, label: str, debit: Decimal = Decimal("0"), credit: Decimal = Decimal("0")):
    entry.lines.append(
        models.JournalLine(
            account=account,
            label=label,
            debit=debit,
            credit=credit,
        )
    )


def post_customer_invoice(session: Session, invoice: models.Invoice, revenue_account: str = "707", vat_account: str = "4457", ar_account: str = "3421"):
    entry = create_entry(
        session,
        tenant_id=invoice.tenant_id,
        reference=invoice.number,
        date=invoice.date,
        description=f"Facture client {invoice.number}",
    )
    add_line(entry, ar_account, "Client", debit=invoice.total_ttc)
    add_line(entry, revenue_account, "Ventes", credit=invoice.total_ht)
    add_line(entry, vat_account, "TVA collectée", credit=invoice.total_tva)
    return entry


def post_payment(session: Session, payment: models.Payment, bank_account: str = "5121", ar_account: str = "3421"):
    entry = create_entry(
        session,
        tenant_id=payment.tenant_id,
        reference=f"ENC-{payment.id}",
        date=payment.date,
        description=f"Encaissement facture {payment.invoice_id}",
    )
    add_line(entry, bank_account, "Banque", debit=payment.amount)
    add_line(entry, ar_account, "Client", credit=payment.amount)
    return entry


def post_stock_delivery(session: Session, tenant_id: int, reference: str, date, cost: Decimal, stock_account: str = "3111", cogs_account: str = "6111"):
    entry = create_entry(
        session,
        tenant_id=tenant_id,
        reference=reference,
        date=date,
        description=f"Sortie stock {reference}",
    )
    add_line(entry, cogs_account, "Coût des ventes", debit=cost)
    add_line(entry, stock_account, "Stock marchandises", credit=cost)
    return entry
