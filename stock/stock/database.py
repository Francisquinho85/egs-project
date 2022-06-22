from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# "postgresql://app_stock:app_stock@db-stock-ticketing:5432/app_stock"
SQLALCHEMY_DATABASE_URL = ""
# SQLALCHEMY_DATABASE_URL = "postgresql://app_stock:app_stock@db:5432/app_stock"

with open("/tmp/secrets/secret", 'r') as f:
    SQLALCHEMY_DATABASE_URL = f.read().strip()


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
