from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text

from settings import HOST, PORT, DATABASE

#engine = create_engine(f'postgresql+psycopg2://postgres:1234@{HOST}:5432/deliveryfood')
engine = create_engine(f'postgresql+psycopg2://postgres:1234@{HOST}:{PORT}/{DATABASE}')

Session = sessionmaker(bind=engine)
Base = declarative_base()



def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
