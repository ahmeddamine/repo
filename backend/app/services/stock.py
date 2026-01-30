from decimal import Decimal

from sqlalchemy.orm import Session

from app import models


def record_receipt(session: Session, tenant_id: int, item: models.Item, quantity: Decimal, unit_cost: Decimal, reference: str, date):
    if quantity <= 0:
        raise ValueError("La quantité reçue doit être positive.")
    total_cost = (item.avg_cost * item.stock_on_hand) + (unit_cost * quantity)
    new_stock = item.stock_on_hand + quantity
    item.avg_cost = (total_cost / new_stock) if new_stock else Decimal("0")
    item.stock_on_hand = new_stock
    movement = models.StockMovement(
        tenant_id=tenant_id,
        item_id=item.id,
        date=date,
        movement_type="receipt",
        quantity=quantity,
        unit_cost=unit_cost,
        reference=reference,
    )
    session.add(movement)


def record_delivery(session: Session, tenant_id: int, item: models.Item, quantity: Decimal, reference: str, date):
    if quantity <= 0:
        raise ValueError("La quantité livrée doit être positive.")
    if item.stock_on_hand < quantity:
        raise ValueError("Stock insuffisant pour la livraison.")
    item.stock_on_hand = item.stock_on_hand - quantity
    movement = models.StockMovement(
        tenant_id=tenant_id,
        item_id=item.id,
        date=date,
        movement_type="delivery",
        quantity=-quantity,
        unit_cost=item.avg_cost,
        reference=reference,
    )
    session.add(movement)
    return item.avg_cost * quantity
