from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()
PWD = os.getenv('PWD')
import sys
sys.path.insert(1, PWD)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{PWD}/data_base/sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
