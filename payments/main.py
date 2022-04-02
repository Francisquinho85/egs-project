
#run this program with python3.7 -m uvicorn main:app --reload
# main.py
from ctypes.util import find_library
import models
from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
import json
from fastapi_versioning import VersionedFastAPI, version
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from models import Payments
from datetime import date

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# valor a pagar, numerario/mb/...
class Payment(BaseModel):
    amount: float
    payMethod: str
    nif: Optional[int] = None
    date: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post("/registPayments")
@version(1)
def regist_payments(payment_request: Payment, db: Session = Depends(get_db)):

    payment = Payments()

    payment.amount = payment_request.amount
    payment.date = payment_request.date
    # if payment_request.date:
    #     payment.date = payment_request.date
    # else:
    #     today = date.today()
    #     # dd-mm-YY
    #     d1 = today.strftime("%d-%m-%Y")
    #     payment.date = d1
    payment.nif = payment_request.nif
    payment.payMethod = payment_request.payMethod

    db.commit()

    return {
        "code" : "success",
        "message" : "payments registed"
    }


# byConsumer,byDay,byHour
@app.get("/transactions")
@version(1)
def list_transactions(by: str):
    # if by == "Consumer":
    # if by == "Day":
    # if by == "Hour":
    # if by == "intervalo de montates"
    return {"item_list": "ALLLL12312312"}
# @app.delete("/event/{event_id}")
# @version(1)
# def delete_event(event_id: int):
#     if event_id in events:
#         del events[event_id]
#         return {"Success": "Event deleted"}
#     return {"Error:" "Event ID not found"}

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')

