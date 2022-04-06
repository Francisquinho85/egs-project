
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
async def list_transactions(list_by: str,list_value: str,list_value2: str=None, db: Session = Depends(get_db)):
    if list_by == "Amount" and list_value2 == None:
        event = db.query(models.Payments).filter(models.Payments.amount == list_value).all()
        if not event:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Events with the amount {list_value} is not available")
        return event
    if list_by == "NIF":
        event = db.query(models.Payments).filter(models.Payments.nif == list_value).all()
        if not event:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Events with the NIF {list_value} is not available")
        return event
    if list_by == "Day" and list_value2 == None:
        dia = db.query(models.Payments).filter(models.Payments.date==list_value).all()
        if not dia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No day found')
        return dia
    if list_by == "Hour" and list_value2 == None:
        hour = db.query(models.Payments).filter(models.Payments.hour==list_value).all()
        if not hour:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Hour not avaliable')
        return hour
    if list_by == "Amounts":
        amounts = db.query(models.Payments).filter(Payments.amount.between(list_value,list_value2)).all()
        if not amounts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'This interval of amounts is not avaliable')
        return amounts
    #if list_by == "Dates":
    #    dates = db.query(models.Payments).filter(Payments.date.between(list_value,list_value2)).all()
    #    if not dates:
    #        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'This interval of dates is not avaliable')
    #    return dates

        

@app.delete("/deletePayment")
@version(1)
def delete_payment(delete_request: Payment, db: Session = Depends(get_db)):

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

