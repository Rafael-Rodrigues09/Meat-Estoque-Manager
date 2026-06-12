from sqlalchemy import create_engine, String, Float, Integer, Column, select, update
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
from datetime import date
from fastapi.responses import FileResponse

def connect():
    load_dotenv()
    url = os.getenv('DATA_URL')
    engine = create_engine(url)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()
    return Base, engine, SessionLocal

Base, engine, SessionLocal = connect()
class Carnes(Base):
    __tablename__ = 'carnes'
    id = Column(Integer, primary_key=True)
    carne = Column(String(40))
    usado_kg = Column(Float)
    sobra_kg = Column(Float)

def criar_banco():
    lista_carnes = [
    ("ACEM", 0.0, 0.0),
    ("ALCATRA COMPLETA", 0, 0.0),
    ("ANCHO", 0.0, 0.0),
    ("ASA DE FRANGO", 0.0, 0.0),
    ("BABY BEEF", 0.0, 0.0),
    ("BIFE DO VAZIO", 0.0, 0.0),
    ("CAPA DO FILÉ", 0.0, 0.0),
    ("CARRÉ DE CARNEIRO", 0.0, 0.0),
    ("CHORIZO", 0.0, 0.0),
    ("CONTRA FILÉ", 0.0, 0.0),
    ("COPA LOMBO (JAVALI)", 0.0, 0.0),
    ("CORAÇÃO DE FRANGO", 0.0, 0.0),
    ("COSTELA DE CARNEIRO", 0.0, 0.0),
    ("COSTELA JANELA", 0.0, 0.0),
    ("COSTELA MINGA", 0.0, 0.0),
    ("COSTELA PRIME", 0.0, 0.0),
    ("COSTELA SUÍNA", 0.0, 0.0),
    ("COXA SOBRE COXA", 0.0, 0.0),
    ("COXÃO MOLE", 0.0, 0.0),
    ("CUPIM", 0.0, 0.0),
    ("FILÉ DE FRANGO", 0.0, 0.0),
    ("FILÉ MIGNON", 0.0, 0.0),
    ("FRALDINHA", 0.0, 0.0),
    ("LAGARTO", 0.0, 0.0),
    ("LINGUIÇA", 0.0, 0.0),
    ("LINGUIÇA APIMENTADA", 0.0, 0.0),
    ("PALETA CARNEIRO", 0.0, 0.0),
    ("PANCETA", 0.0, 0.0),
    ("PICANHA", 0.0, 0.0),
    ("PICANHA FATIADA", 0.0, 0.0),
    ("PONTA DE PEITO", 0.0, 0.0),
    ("PRIME", 0.0, 0.0),
    ("QUEIJO", 0.0, 0.0),
    ("SHOT RIBY", 0.0, 0.0),
    ("T BONE CARNEIRO", 0.0, 0.0),
    ("THIBON BOVINO", 0.0, 0.0),
    ("MAMINHA", 0.0, 0.0),
    ("LINGUIÇA CUIABANA", 0.0, 0.0),
    ("PERNIL DE CARNEIRO", 0.0, 0.0)
    ]
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        query = select(Carnes)
        carnes = session.scalars(query).first()
        if carnes == None:
            for carne, usado, sobra in lista_carnes:
                  nova_carne = Carnes(carne=carne, usado_kg=usado, sobra_kg=sobra)
                  session.add(nova_carne)
            session.commit()

def show_data():
    with SessionLocal() as session:
        query = select(Carnes)
        result = session.scalars(query).all()
        dict = {}
        for carne in result:
            dict[carne.carne] = {'usado_kg': carne.usado_kg, 'sobra_kg': carne.sobra_kg}
        return dict

def add_usado(carne_nome, valor):
    with SessionLocal() as session:
        carne_query = select(Carnes).where(Carnes.carne == carne_nome)
        carne = session.scalars(carne_query).first()
        if carne:
            carne.usado_kg += valor
            session.commit()
            return {'status': 'success'}
        else:
            return {'status': 'invalid'}
    
    
def add_sobra(carne_nome, valor):
    with SessionLocal() as session:
        carne_query = select(Carnes).where(Carnes.carne == carne_nome)
        carne = session.scalars(carne_query).first()
        if carne:
            carne.sobra_kg += valor
            session.commit()
            return {'status': 'success'}
        else:
            return {'status': 'invalid'}
        
def reset():
    with SessionLocal() as session:
        query_values = select(Carnes.carne, Carnes.usado_kg, Carnes.sobra_kg)
        values = session.execute(query_values).all()
        with open(f'backup.txt', 'w', encoding='UTF-8') as backup:
            for carne, usado, sobra in values:
                if usado != 0.0 or sobra != 0.0:
                    backup.write(f'{carne}: usado_kg {usado} --- sobra_kg {sobra}\n')
        session.execute(
            update(Carnes).values(
                usado_kg=0.0,
                sobra_kg=0.0
            )
        )
        session.commit()
        return FileResponse(path='backup.txt', filename=f'Backup{date.today()}.txt', media_type='text/plain')
    
    
          
               

     
        




