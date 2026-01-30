import sys
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models, schemas
from app.db import Base
from app.services import workflow


class SalesWorkflowTestCase(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        self.SessionLocal = sessionmaker(bind=engine)
        self.session = self.SessionLocal()

        tenant = models.Tenant(
            name="Test SARL",
            if_number="IF1",
            ice_number="ICE1",
            address="Rue Test",
        )
        self.session.add(tenant)
        self.session.flush()
        self.tenant_id = tenant.id

        tax = models.TaxRate(tenant_id=tenant.id, name="TVA 20%", rate=Decimal("20.00"), is_default=True)
        self.session.add(tax)
        self.session.flush()
        self.tax_id = tax.id

        client = models.Client(
            tenant_id=tenant.id,
            name="Client Test",
            if_number="IF2",
            ice_number="ICE2",
            address="Rue Client",
        )
        self.session.add(client)
        self.session.flush()
        self.client_id = client.id

        item = models.Item(
            tenant_id=tenant.id,
            sku="SKU1",
            name="Produit",
            unit="UN",
            price=Decimal("100.00"),
            tax_rate_id=tax.id,
            avg_cost=Decimal("60.00"),
            stock_on_hand=Decimal("10.00"),
        )
        self.session.add(item)
        self.session.commit()
        self.item_id = item.id

    def tearDown(self):
        self.session.close()

    def test_full_sales_workflow(self):
        quote_payload = schemas.QuoteCreate(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            number="DEV-1",
            date=date(2025, 1, 15),
            lines=[
                schemas.QuoteLineCreate(
                    item_id=self.item_id,
                    description="Produit",
                    quantity=Decimal("2.00"),
                    unit_price=Decimal("100.00"),
                    tax_rate_id=self.tax_id,
                )
            ],
        )
        quote = workflow.create_quote(self.session, quote_payload)
        self.session.flush()

        order = workflow.confirm_quote_to_order(self.session, quote, order_number="BC-1")
        self.session.flush()

        delivery = workflow.create_delivery(
            self.session,
            tenant_id=self.tenant_id,
            sales_order=order,
            number="BL-1",
            date=date(2025, 1, 16),
        )
        self.session.flush()

        invoice_payload = schemas.InvoiceCreate(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            number="FA-1",
            date=date(2025, 1, 17),
            due_date=date(2025, 2, 17),
            lines=[
                schemas.InvoiceLineCreate(
                    item_id=self.item_id,
                    description="Produit",
                    quantity=Decimal("2.00"),
                    unit_price=Decimal("100.00"),
                    tax_rate_id=self.tax_id,
                )
            ],
        )
        invoice = workflow.create_invoice(self.session, invoice_payload)
        self.session.flush()

        payment_payload = schemas.PaymentCreate(
            tenant_id=self.tenant_id,
            invoice_id=invoice.id,
            date=date(2025, 1, 20),
            amount=invoice.total_ttc,
        )
        payment = workflow.register_payment(self.session, payment_payload)
        self.session.commit()

        self.assertEqual(delivery.status, "delivered")
        self.assertEqual(invoice.status, "paid")
        self.assertEqual(payment.amount, Decimal("240.00"))


if __name__ == "__main__":
    unittest.main()
