from decimal import Decimal

from sqlalchemy.orm import Session

from app import models
from app.services import posting, stock


def create_quote(session: Session, payload):
    quote = models.Quote(
        tenant_id=payload.tenant_id,
        client_id=payload.client_id,
        number=payload.number,
        date=payload.date,
        status="draft",
    )
    for line in payload.lines:
        quote.lines.append(
            models.QuoteLine(
                item_id=line.item_id,
                description=line.description,
                quantity=line.quantity,
                unit_price=line.unit_price,
                tax_rate_id=line.tax_rate_id,
            )
        )
    session.add(quote)
    return quote


def confirm_quote_to_order(session: Session, quote: models.Quote, order_number: str):
    sales_order = models.SalesOrder(
        tenant_id=quote.tenant_id,
        client_id=quote.client_id,
        number=order_number,
        date=quote.date,
        status="confirmed",
    )
    for line in quote.lines:
        sales_order.lines.append(
            models.SalesOrderLine(
                item_id=line.item_id,
                description=line.description,
                quantity=line.quantity,
                unit_price=line.unit_price,
                tax_rate_id=line.tax_rate_id,
            )
        )
    quote.status = "converted"
    session.add(sales_order)
    return sales_order


def create_delivery(session: Session, tenant_id: int, sales_order: models.SalesOrder, number: str, date):
    delivery = models.Delivery(
        tenant_id=tenant_id,
        sales_order_id=sales_order.id,
        number=number,
        date=date,
        status="delivered",
    )
    total_cost = Decimal("0")
    for line in sales_order.lines:
        delivery.lines.append(
            models.DeliveryLine(
                item_id=line.item_id,
                description=line.description,
                quantity=line.quantity,
            )
        )
        item = session.get(models.Item, line.item_id)
        total_cost += stock.record_delivery(
            session,
            tenant_id=tenant_id,
            item=item,
            quantity=line.quantity,
            reference=number,
            date=date,
        )
    posting.post_stock_delivery(session, tenant_id=tenant_id, reference=number, date=date, cost=total_cost)
    session.add(delivery)
    return delivery


def create_invoice(session: Session, payload):
    invoice = models.Invoice(
        tenant_id=payload.tenant_id,
        client_id=payload.client_id,
        number=payload.number,
        date=payload.date,
        due_date=payload.due_date,
        status="posted",
    )
    total_ht = Decimal("0")
    total_tva = Decimal("0")
    for line in payload.lines:
        invoice.lines.append(
            models.InvoiceLine(
                item_id=line.item_id,
                description=line.description,
                quantity=line.quantity,
                unit_price=line.unit_price,
                tax_rate_id=line.tax_rate_id,
            )
        )
        line_total = line.quantity * line.unit_price
        tax_rate = session.get(models.TaxRate, line.tax_rate_id)
        tax_amount = (line_total * tax_rate.rate) / Decimal("100")
        total_ht += line_total
        total_tva += tax_amount
    invoice.total_ht = total_ht
    invoice.total_tva = total_tva
    invoice.total_ttc = total_ht + total_tva
    session.add(invoice)
    posting.post_customer_invoice(session, invoice)
    return invoice


def register_payment(session: Session, payload):
    payment = models.Payment(
        tenant_id=payload.tenant_id,
        invoice_id=payload.invoice_id,
        date=payload.date,
        amount=payload.amount,
        method=payload.method,
    )
    session.add(payment)
    posting.post_payment(session, payment)
    invoice = session.get(models.Invoice, payload.invoice_id)
    invoice.status = "paid"
    return payment
