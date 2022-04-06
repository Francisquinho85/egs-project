
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
from datetime import *
from fastapi import HTTPException, status

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
    date: Optional[str] = None
    hour: Optional[str] = None

class ListRequest(BaseModel):
    list_by: str
    list_value: str

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
    
    #se nao especificar data fica com a data atual e hora igual

    #   xx-xx-xxxx    
    if payment_request.date:
        payment.date = payment_request.date
    else:
        today = date.today()
        #dd-mm-YY
        d1 = today.strftime("%d-%m-%Y")
        payment.date = d1

    #   XX:XX
    if payment_request.hour:
        payment.hour = payment_request.hour
    else:
        time = datetime.strptime("03/02/21 16:30", "%d/%m/%y %H:%M")
        time = ("{:d}:{:02d}".format(time.hour, time.minute))
        payment.hour = time
    payment.nif = payment_request.nif
    payment.payMethod = payment_request.payMethod

    db.add(payment)
    db.commit()

    return {
        "code" : "success",
        "message" : "payments registed"
    }


# byConsumer,byDay,byHour
@app.get("/transactions")
@version(1)
async def list_transactions(list_request: ListRequest, db: Session = Depends(get_db)):
    if list_request.list_by == "Consumer":
        #return print(db.query(models.Payments).filter(models.Payments.hour==hora))
        return {
            "code" : "success",
            "message" : "Consumidor"
        }
    if list_request.list_by == "Day":
        dia = db.query(models.Payments).filter(models.Payments.date==list_request.list_value).first()
        if not dia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No day found')
        return dia
    # if by == "Hour":
    # if by == "intervalo de montates"

@app.delete("/event/{event_id}")
@version(1)
def delete_event(delete_request: Payment, db: Session = Depends(get_db)):

    event = db.query(models.Payments).filter(models.Payments.amount == delete_request.amount,models.Payments.payMethod==delete_request.payMethod,models.Payments.date==delete_request.date,
    models.Payments.hour==delete_request.hour,models.Payments.nif==delete_request.nif)

    event.delete(synchronize_session=False)

    db.commit()

    return {
        "code": "success",
        "message": "Event Deleted"
    }

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')

