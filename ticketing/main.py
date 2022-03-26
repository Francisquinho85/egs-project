#run this program with python3 -m uvicorn main:app --reload


from fastapi import FastAPI, Path
from pydantic import BaseModel
from enum import Enum
from fastapi_versioning import VersionedFastAPI, version
from typing import Optional

app = FastAPI()

tickets = {}
events = {}

class Event(BaseModel):
    name: str
    location: str
    date: int
    number_tickets: int
    ticket_price: float

class UpdateEvent(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    date: Optional[int] = None
    number_tickets: Optional[int] = None
    ticket_price: Optional[float] = None

class TicketStatus(int, Enum):
    free = "0"
    reserved = "1"
    paid = "2"

class Ticket(BaseModel):
    event_id: int
    nif: int
    status: Optional[TicketStatus] = 1
    name: Optional[str] = None

@app.get("/event/{event_id}")
@version(1)
def get_event(event_id: int):
    if event_id in events:
        return events[event_id]
    return {"Error": "Event ID not found"}

@app.post("/event/")
@version(1)
def create_event(event: Event, event_id: int = Path(..., description="The ID of the event to create")):
    if event_id in events:
        return {"Error: Event ID already exists"}
    events[event_id] = event
    return events[event_id]

@app.put("/event/{event_id}")
@version(1)
def update_event(event_id: int, event: UpdateEvent):
    if event_id not in events:
        return {"Error: Event ID does not exist"}

    if event.name != None:
        events[event_id].name = event.name
    if event.location != None:
        events[event_id].location = event.location
    if event.date != None:
        events[event_id].date = event.date
    if event.ticket_price != None:
        events[event_id].price = event.ticket_price
    if event.number_tickets != None:
        events[event_id].tickets = event.number_tickets
    return events[event_id]

@app.delete("/event/{event_id}")
@version(1)
def delete_event(event_id: int):
    if event_id in events:
        del events[event_id]
        return {"Success": "Event deleted"}
    return {"Error:" "Event ID not found"}

@app.post("/ticket/")
@version(1)
def buy_ticket(ticket: Ticket, ticket_id: int):
    if ticket_id in tickets:
        return {"Error": "Ticket ID already exists"}
    tickets[ticket_id] = ticket
    return tickets[ticket_id]

@app.get("/ticket/{ticket_id}")
@version(1)
def get_ticket(ticket_id: int):
    if ticket_id in tickets:
        return tickets[ticket_id]
    return {"Error": "Ticket ID not found" }

@app.put("/ticket/{ticket_id}/")
@version(1)
def update_ticket(ticket_id: int, ticket: Ticket):
    if ticket_id not in tickets:
        return {"Error": "Ticket ID not found" }

    if ticket.nif != None:
        tickets[ticket_id].nif = ticket.nif
    if ticket.status != None:
        tickets[ticket_id].status = ticket.status
    if ticket.name != None:
        tickets[ticket_id].name = ticket.name
    return tickets[ticket_id]

@app.post("/ticket/pay")
@version(1)
def buy_ticket(ticket: Ticket, ticket_id: int):
    if ticket_id in tickets:
        return {"Error": "Ticket ID already exists"}
    tickets[ticket_id] = ticket
    return tickets[ticket_id]

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')