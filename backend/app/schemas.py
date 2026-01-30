from datetime import date
from decimal import Decimal
from typing import List

from pydantic import BaseModel


class ClientCreate(BaseModel):
    tenant_id: int
    name: str
    if_number: str
    ice_number: str
    address: str
    payment_terms_days: int = 30


class ItemCreate(BaseModel):
    tenant_id: int
    sku: str
    name: str
    unit: str = "UN"
    price: Decimal
    tax_rate_id: int


class QuoteLineCreate(BaseModel):
    item_id: int
    description: str
    quantity: Decimal
    unit_price: Decimal
    tax_rate_id: int


class QuoteCreate(BaseModel):
    tenant_id: int
    client_id: int
    number: str
    date: date
    lines: List[QuoteLineCreate]


class SalesOrderCreate(BaseModel):
    tenant_id: int
    client_id: int
    number: str
    date: date
    lines: List[QuoteLineCreate]


class DeliveryLineCreate(BaseModel):
    item_id: int
    description: str
    quantity: Decimal


class DeliveryCreate(BaseModel):
    tenant_id: int
    sales_order_id: int
    number: str
    date: date
    lines: List[DeliveryLineCreate]


class InvoiceLineCreate(BaseModel):
    item_id: int
    description: str
    quantity: Decimal
    unit_price: Decimal
    tax_rate_id: int


class InvoiceCreate(BaseModel):
    tenant_id: int
    client_id: int
    number: str
    date: date
    due_date: date
    lines: List[InvoiceLineCreate]


class PaymentCreate(BaseModel):
    tenant_id: int
    invoice_id: int
    date: date
    amount: Decimal
    method: str = "virement"
