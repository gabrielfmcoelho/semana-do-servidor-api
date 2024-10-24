from .database import get_database_interface
from sqlalchemy.sql.expression import func
from datetime import datetime as dt
from .schemas import Pessoa

class PessoaRepository:
    def __init__(self):
        self.db_interface = get_database_interface()

    def get_pessoas(self):
        with self.db_interface.get_session() as session:
            return session.query(Pessoa).filter(Pessoa.duplicado == 0).all()

    def get_validated_pessoas(self):
        with self.db_interface.get_session() as session:
            return session.query(Pessoa).filter(Pessoa.dataValidacao != None, Pessoa.duplicado == 0).all()

    def get_pessoa(self, cpf: str):
        with self.db_interface.get_session() as session:
            return session.query(Pessoa).filter(Pessoa.cpf == cpf, Pessoa.duplicado == 0).first()
        
    def validate_pessoa(self, cpf: str, force: bool = False):
        with self.db_interface.get_session() as session:
            pessoa = session.query(Pessoa).filter(Pessoa.cpf == cpf, Pessoa.duplicado == 0).first()
            if pessoa:
                pessoa.dataValidacao = dt.now()
                session.commit()
                return True
            elif force:
                pessoa = Pessoa(cpf=cpf, dataValidacao=dt.now(), sorteado=0, duplicado=0)
                session.add(pessoa)
                session.commit()
                return True
            return False
        
    def draw_random_pessoa(self):
        with self.db_interface.get_session() as session:
            pessoa = session.query(Pessoa).filter(Pessoa.dataValidacao != None, Pessoa.sorteado == 0, Pessoa.duplicado == 0).order_by(func.random()).first()
            if pessoa:
                pessoa.sorteado = 1
                print(pessoa.nome)
                pessoa_cpf = pessoa.cpf
                print(pessoa_cpf)
                session.commit()
                return pessoa_cpf
            return None
        
    def get_draw_pessoa(self):
        with self.db_interface.get_session() as session:
            return session.query(Pessoa).filter(Pessoa.dataValidacao != None, Pessoa.sorteado == 1, Pessoa.duplicado == 0).all()
        
    def clean_validated(self):
        with self.db_interface.get_session() as session:
            session.query(Pessoa).update({Pessoa.dataValidacao: None})
            session.commit()
    
    def clean_drawn(self):
        with self.db_interface.get_session() as session:
            session.query(Pessoa).update({Pessoa.sorteado: 0})
            session.commit()