from .database import get_database_interface
from sqlalchemy import Table

db_interface = get_database_interface()

Base = db_interface.get_declarative_base()
engine = db_interface.get_engine()
metadata = db_interface.get_metadata()

class Pessoa(Base):
    __table__ = Table('pessoa', metadata, autoload_with=engine)