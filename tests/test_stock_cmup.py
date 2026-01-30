import sys
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.db import Base
from app.services import stock


class StockCMUPTestCase(unittest.TestCase):
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

        self.item = models.Item(
            tenant_id=tenant.id,
            sku="SKU1",
            name="Produit",
            unit="UN",
            price=Decimal("100.00"),
            tax_rate_id=tax.id,
            avg_cost=Decimal("50.00"),
            stock_on_hand=Decimal("10.00"),
        )
        self.session.add(self.item)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_cmup_recalculation(self):
        stock.record_receipt(
            self.session,
            tenant_id=self.tenant_id,
            item=self.item,
            quantity=Decimal("5.00"),
            unit_cost=Decimal("70.00"),
            reference="RCPT-1",
            date=date(2025, 1, 5),
        )
        self.session.commit()

        expected_avg_cost = (Decimal("10.00") * Decimal("50.00") + Decimal("5.00") * Decimal("70.00")) / Decimal("15.00")
        self.assertEqual(self.item.avg_cost, expected_avg_cost)
        self.assertEqual(self.item.stock_on_hand, Decimal("15.00"))


if __name__ == "__main__":
    unittest.main()
