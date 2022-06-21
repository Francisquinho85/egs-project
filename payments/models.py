from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Numeric

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10,2),index=True)   
    payMethod = Column(String(16))
    nif = Column(Integer)
    date = Column(Date)
    hour = Column(String(5))


#https://youtu.be/ESVwKQLldjg?t=450