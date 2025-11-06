from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/deliveryfood')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Importar los modelos
from models.domain.carta import Carta

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
