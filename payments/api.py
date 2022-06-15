import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

# Define the MariaDB engine using MariaDB Connector/Python

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://couto:couto123@127.0.0.1:3306/payments")