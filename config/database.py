from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text

# cambiar el nombre de localhost al nombre del contenedor de la db dentro de la misma red de docker
engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432/deliveryfood')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Importar los modelos
#from models.domain.carta import Carta

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
