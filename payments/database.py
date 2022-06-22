# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./payments.db"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the MariaDB engine using MariaDB Connector/Python

#engine = sqlalchemy.create_engine("mariadb+mariadbconnector://couto:couto123@db-payments:3306/db-payments")

SQLALCHEMY_DATABASE_URL = ""

with open("/tmp/secrets/payments-secret", 'r') as f:
    SQLALCHEMY_DATABASE_URL = f.read().strip()

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)