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
from app.services import posting


class PostingEngineTestCase(unittest.TestCase):
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
        self.session.commit()
        self.tenant_id = tenant.id

    def tearDown(self):
        self.session.close()

    def test_customer_invoice_balanced(self):
        invoice = models.Invoice(
            tenant_id=self.tenant_id,
            client_id=1,
            number="FA-1",
            date=date(2025, 1, 10),
            due_date=date(2025, 2, 10),
            total_ht=Decimal("1000.00"),
            total_tva=Decimal("200.00"),
            total_ttc=Decimal("1200.00"),
        )
        entry = posting.post_customer_invoice(self.session, invoice)
        self.session.add(entry)
        self.session.commit()

        debit = sum(line.debit for line in entry.lines)
        credit = sum(line.credit for line in entry.lines)
        self.assertEqual(debit, credit)


if __name__ == "__main__":
    unittest.main()
