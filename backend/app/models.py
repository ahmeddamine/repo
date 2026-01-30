from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    if_number = Column(String(50), nullable=False)
    ice_number = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship("Tenant")


class TaxRate(Base):
    __tablename__ = "tax_rates"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    rate = Column(Numeric(5, 2), nullable=False)
    is_default = Column(Boolean, default=False)

    tenant = relationship("Tenant")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(200), nullable=False)
    if_number = Column(String(50), nullable=False)
    ice_number = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    payment_terms_days = Column(Integer, default=30)

    tenant = relationship("Tenant")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(200), nullable=False)
    if_number = Column(String(50), nullable=False)
    ice_number = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)

    tenant = relationship("Tenant")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    sku = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)
    unit = Column(String(20), default="UN")
    price = Column(Numeric(12, 2), nullable=False)
    tax_rate_id = Column(Integer, ForeignKey("tax_rates.id"), nullable=False)
    avg_cost = Column(Numeric(12, 2), default=0)
    stock_on_hand = Column(Numeric(12, 2), default=0)

    tenant = relationship("Tenant")
    tax_rate = relationship("TaxRate")


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    number = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(30), default="draft")

    tenant = relationship("Tenant")
    client = relationship("Client")
    lines = relationship("QuoteLine", back_populates="quote", cascade="all, delete-orphan")


class QuoteLine(Base):
    __tablename__ = "quote_lines"

    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    description = Column(String(200), nullable=False)
    quantity = Column(Numeric(12, 2), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    tax_rate_id = Column(Integer, ForeignKey("tax_rates.id"), nullable=False)

    quote = relationship("Quote", back_populates="lines")
    item = relationship("Item")
    tax_rate = relationship("TaxRate")


class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    number = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(30), default="draft")

    tenant = relationship("Tenant")
    client = relationship("Client")
    lines = relationship("SalesOrderLine", back_populates="sales_order", cascade="all, delete-orphan")


class SalesOrderLine(Base):
    __tablename__ = "sales_order_lines"

    id = Column(Integer, primary_key=True)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    description = Column(String(200), nullable=False)
    quantity = Column(Numeric(12, 2), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    tax_rate_id = Column(Integer, ForeignKey("tax_rates.id"), nullable=False)

    sales_order = relationship("SalesOrder", back_populates="lines")
    item = relationship("Item")
    tax_rate = relationship("TaxRate")


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=False)
    number = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(30), default="draft")

    tenant = relationship("Tenant")
    sales_order = relationship("SalesOrder")
    lines = relationship("DeliveryLine", back_populates="delivery", cascade="all, delete-orphan")


class DeliveryLine(Base):
    __tablename__ = "delivery_lines"

    id = Column(Integer, primary_key=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    description = Column(String(200), nullable=False)
    quantity = Column(Numeric(12, 2), nullable=False)

    delivery = relationship("Delivery", back_populates="lines")
    item = relationship("Item")


class Invoice(Base):
    __tablename__ = "invoices"

    __table_args__ = (
        CheckConstraint("total_ht >= 0"),
        CheckConstraint("total_tva >= 0"),
        CheckConstraint("total_ttc >= 0"),
    )

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    number = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String(30), default="draft")
    total_ht = Column(Numeric(12, 2), default=0)
    total_tva = Column(Numeric(12, 2), default=0)
    total_ttc = Column(Numeric(12, 2), default=0)

    tenant = relationship("Tenant")
    client = relationship("Client")
    lines = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    description = Column(String(200), nullable=False)
    quantity = Column(Numeric(12, 2), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    tax_rate_id = Column(Integer, ForeignKey("tax_rates.id"), nullable=False)

    invoice = relationship("Invoice", back_populates="lines")
    item = relationship("Item")
    tax_rate = relationship("TaxRate")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    method = Column(String(50), default="virement")

    tenant = relationship("Tenant")
    invoice = relationship("Invoice")


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    reference = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship("Tenant")
    lines = relationship("JournalLine", back_populates="entry", cascade="all, delete-orphan")


class JournalLine(Base):
    __tablename__ = "journal_lines"

    id = Column(Integer, primary_key=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)
    account = Column(String(20), nullable=False)
    label = Column(String(200), nullable=False)
    debit = Column(Numeric(12, 2), default=0)
    credit = Column(Numeric(12, 2), default=0)

    entry = relationship("JournalEntry", back_populates="lines")


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    date = Column(Date, nullable=False)
    movement_type = Column(String(30), nullable=False)
    quantity = Column(Numeric(12, 2), nullable=False)
    unit_cost = Column(Numeric(12, 2), nullable=False)
    reference = Column(String(50), nullable=False)

    tenant = relationship("Tenant")
    item = relationship("Item")
