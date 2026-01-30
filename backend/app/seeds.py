from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app import models


def seed_demo(session: Session):
    tenant = models.Tenant(
        name="Atlas Industrie SARL",
        if_number="IF1234567",
        ice_number="ICE001234567000",
        address="12 Rue Oued Ziz, Casablanca",
    )
    session.add(tenant)
    session.flush()

    tax_20 = models.TaxRate(tenant_id=tenant.id, name="TVA 20%", rate=Decimal("20.00"), is_default=True)
    tax_10 = models.TaxRate(tenant_id=tenant.id, name="TVA 10%", rate=Decimal("10.00"))
    session.add_all([tax_20, tax_10])
    session.flush()

    client = models.Client(
        tenant_id=tenant.id,
        name="Riad Distribution",
        if_number="IF7654321",
        ice_number="ICE009876543000",
        address="Lot 4, Hay Riad, Rabat",
        payment_terms_days=30,
    )
    session.add(client)
    session.flush()

    item = models.Item(
        tenant_id=tenant.id,
        sku="PRD-CHAIR",
        name="Chaise bureau Atlas",
        unit="UN",
        price=Decimal("1200.00"),
        tax_rate_id=tax_20.id,
        avg_cost=Decimal("750.00"),
        stock_on_hand=Decimal("25.00"),
    )
    session.add(item)
    session.flush()

    quote = models.Quote(
        tenant_id=tenant.id,
        client_id=client.id,
        number="DEV-2025-0001",
        date=date(2025, 1, 15),
        status="draft",
    )
    quote.lines.append(
        models.QuoteLine(
            item_id=item.id,
            description="Chaise bureau Atlas",
            quantity=Decimal("10.00"),
            unit_price=Decimal("1200.00"),
            tax_rate_id=tax_20.id,
        )
    )
    session.add(quote)
    session.commit()

    return {"tenant_id": tenant.id, "client_id": client.id, "item_id": item.id}
