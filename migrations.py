from sqlalchemy import create_engine, Column, Integer, String, Boolean
from db import engine
import sqlalchemy

Base = sqlalchemy.orm.declarative_base()
    
Base.metadata.create_all(bind=engine)