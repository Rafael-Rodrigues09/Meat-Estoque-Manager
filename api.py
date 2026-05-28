import psycopg2
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import date

def connect_banco():
    conexao = psycopg2.connect(
        host='localhost',
        port='5432',
        user='postgres',
        password='root',
        database='postgres'
    )
    return conexao

def criar_banco():
    conexao = connect_banco()
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS estoque_carnes(
                    id SERIAL PRIMARY KEY,
                    carne TEXT NOT NULL,
                    usado_kg FLOAT NOT NULL,
                    sobra_kg FLOAT NOT NULL
                   )''')
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
    cursor.execute('SELECT COUNT(*) FROM estoque_carnes')
    resultado = cursor.fetchone()
    if resultado[0] == 0:
        comando = ('INSERT INTO estoque_carnes (carne, usado_kg, sobra_kg) VALUES (%s, %s, %s)')
        cursor.executemany(comando, lista_carnes)
    conexao.commit()
    conexao.close()
class ModeloRegistro(BaseModel):
    carne: str
    quantidade: float

app = FastAPI()
criar_banco()
@app.get('/estoque')
def start_estoque():
    conexao = connect_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT carne, usado_kg, sobra_kg FROM estoque_carnes')
    dados = cursor.fetchall()
    dicionario = {}
    for carne, usado, sobra in dados:
        dicionario[carne] = {'usado_kg': usado, 'sobra_kg': sobra}
    conexao.close()
    return dicionario

@app.post('/uso')
def registrar_uso(dados: ModeloRegistro):
    conexao = connect_banco()
    cursor = conexao.cursor()
    comando = ('UPDATE estoque_carnes SET usado_kg = usado_kg + %s WHERE carne = %s')
    valores = (dados.quantidade, dados.carne)
    cursor.execute(comando, valores)
    conexao.commit()
    conexao.close()
    return {'status': 'sucesso', 'msg': f'{dados.quantidade} kg adicionados a {dados.carne}'}
    
    
@app.post('/sobra')
def registrar_sobra(dados: ModeloRegistro):
    conexao = connect_banco()
    cursor = conexao.cursor()
    comando = ('UPDATE estoque_carnes SET sobra_kg = sobra_kg + %s WHERE carne = %s')
    valores = (dados.quantidade, dados.carne)
    cursor.execute(comando, valores)
    conexao.commit()
    conexao.close()
    return {'status': 'sucesso', 'msg': f'{dados.quantidade} kg adicionados a {dados.carne}'}
    

@app.post('/reset')
def reset():
    conexao = connect_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT carne, usado_kg, sobra_kg FROM estoque_carnes')
    dados = cursor.fetchall()
    with open(f'backup.txt', 'w', encoding='UTF-8') as backup:
        for carne, usado, sobra in dados:
            if usado != 0.0 or sobra != 0.0:
                backup.write(f'{carne}: usado_kg {usado} --- sobra_kg {sobra}\n')
    cursor.execute('UPDATE estoque_carnes SET usado_kg = 0.0, sobra_kg = 0.0')
    conexao.commit()
    conexao.close()
    caminho_arquivo = 'backup.txt'
    return FileResponse(path=caminho_arquivo, filename=f'Backup{date.today()}.txt', media_type='text/plain')







