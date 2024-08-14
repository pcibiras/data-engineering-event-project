from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

mysql_user = os.getenv('mysql_user')
mysql_password = os.getenv('mysql_password')
mysql_database = os.getenv('mysql_database')

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

def create_schema(database_url):
    try:
        engine = create_engine(database_url)
        Base.metadata.create_all(engine)
        print("Schema creation successful!")
    except SQLAlchemyError as e:
        print(f"Schema creation failed: {e}")
    

database_url = f'mariadb+mariadbconnector://{mysql_user}:{mysql_password}@127.0.0.1:3306/{mysql_database}'

create_schema(database_url)
