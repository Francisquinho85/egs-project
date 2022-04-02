
#run this program with python3 -m uvicorn main:app --reload
# main.py
import models
from fastapi import FastAPI
from pydantic import BaseModel
import json
from fastapi_versioning import VersionedFastAPI, version
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal,engine

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
    date: int

@app.post("/registPayments")
@version(1)
def regist_payments(amount: float, payMethod: str):
    with open("paymentdb.json","r") as json_file:    
        json_data = json.load(json_file)
    if json_data:
        #check if amount is present
        if json_data.get(amount): 
            return None
    else:
        return None

@app.get("/transactions")
@version(1)
def list_transactions(by: str):
    # if by == "Consumer":
    # if by == "Day":
    # if by == "Hour":
    # if by == "intervalo de montates"
    return {"item_list": "ALLLL12312312"}

#@app.get("/listTransactionsByConsumer")
# @version(1)
# def list_byconsumer(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/listTransactionsByDay")
# @version(1)
# def list_byday(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/listTransactionsByHour")
# @version(1)
# def list_byhour(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
# 

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

