from datetime import date

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import Base, SessionLocal, engine
from app.services import workflow

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AtlasFlow ERP Maroc")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/clients")
def create_client(payload: schemas.ClientCreate, db: Session = Depends(get_db)):
    client = models.Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@app.post("/items")
def create_item(payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = models.Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.post("/quotes")
def create_quote(payload: schemas.QuoteCreate, db: Session = Depends(get_db)):
    quote = workflow.create_quote(db, payload)
    db.commit()
    db.refresh(quote)
    return quote


@app.post("/quotes/{quote_id}/confirm")
def confirm_quote(quote_id: int, order_number: str, db: Session = Depends(get_db)):
    quote = db.get(models.Quote, quote_id)
    order = workflow.confirm_quote_to_order(db, quote, order_number=order_number)
    db.commit()
    db.refresh(order)
    return order


@app.post("/deliveries")
def create_delivery(payload: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    sales_order = db.get(models.SalesOrder, payload.sales_order_id)
    delivery = workflow.create_delivery(db, tenant_id=payload.tenant_id, sales_order=sales_order, number=payload.number, date=payload.date)
    db.commit()
    db.refresh(delivery)
    return delivery


@app.post("/invoices")
def create_invoice(payload: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    invoice = workflow.create_invoice(db, payload)
    db.commit()
    db.refresh(invoice)
    return invoice


@app.post("/payments")
def create_payment(payload: schemas.PaymentCreate, db: Session = Depends(get_db)):
    payment = workflow.register_payment(db, payload)
    db.commit()
    db.refresh(payment)
    return payment


@app.get("/health")
def healthcheck():
    return {"status": "ok", "date": date.today().strftime("%d/%m/%Y")}
