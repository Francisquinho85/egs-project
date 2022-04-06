from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Numeric

from database import Base


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10,2),index=True)   
    payMethod = Column(String)
    nif = Column(Integer)
    date = Column(Date)
    hour = Column(String)


#https://youtu.be/ESVwKQLldjg?t=450