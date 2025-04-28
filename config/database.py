import os
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_HOST = ''

if os.getenv("ENVIRONMENT") == "production":
    DB_HOST = 'mysql.railway.internal'
else:
    DB_HOST = os.getenv("MYSQLHOST")


# Configuración para MySQL
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_PORT = os.getenv("MYSQLPORT")

database_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(database_url, echo=True, pool_timeout=60, pool_size=20, max_overflow=10)

Session = sessionmaker(bind=engine)

Base = declarative_base()

