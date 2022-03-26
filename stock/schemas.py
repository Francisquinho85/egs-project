from pydantic import BaseModel
from typing import Optional

class Provider(BaseModel):
    name: str
    contact: int
    mail: str

class Product(BaseModel):
    name: str
    id: int
    location: str
    price: int
    quantity: int
    type: str
    provider: Provider

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    price: Optional[int] = int
    quantity: Optional[int] = int
    type: Optional[str] = None
    provider: Optional[Provider] = None