from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from stock.database import Base


class Provider(Base):
    __tablename__ = "provider"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact = Column(Integer, unique=True)
    mail = Column(String, unique=True)

    products = relationship("Product", back_populates="provider")


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    type = Column(String)
    provider_id = Column(Integer, ForeignKey("provider.id"))

    provider = relationship("Provider", back_populates="products")
