from pydantic import BaseModel
from typing import Optional

class Provider(BaseModel):
    id: int
    name: str
    contact: int
    mail: str
    class Config:
        orm_mode = True

class Product(BaseModel):
    id: int
    name: str
    location: str
    price: int
    quantity: int
    type: str
    provider: Provider
    class Config:
        orm_mode = True

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    price: Optional[int] = int
    quantity: Optional[int] = int
    type: Optional[str] = None
    provider: Optional[Provider] = None