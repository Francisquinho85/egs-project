from pydantic import BaseModel
from typing import Optional

class Provider(BaseModel):
    name: str
    contact: int
    mail: str
    class Config:
        orm_mode = True

class UpdateProvider(BaseModel):
    name: Optional[str] = None
    contact: Optional[int] = None
    mail: Optional[str] = None

class Product(BaseModel):
    name: str
    location: str
    price: int
    quantity: int
    type: str
    provider_id: int
    class Config:
        orm_mode = True

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    type: Optional[str] = None
    provider_id: Optional[int] = None