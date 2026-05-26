import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

class ModeloRegistro(BaseModel):
    carne: str
    quantidade: float

app = FastAPI()
@app.get('/estoque')
def start_estoque():
    conexao = sqlite3.connect('estoque.db')
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
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    comando = ('UPDATE estoque_carnes SET usado_kg = usado_kg + ? WHERE carne = ?')
    valores = (dados.quantidade, dados.carne)
    cursor.execute(comando, valores)
    conexao.commit()
    conexao.close()
    return {'status': 'sucesso', 'msg': f'{dados.quantidade} kg adicionados a {dados.carne}'}
    
    
@app.post('/sobra')
def registrar_sobra(dados: ModeloRegistro):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    comando = ('UPDATE estoque_carnes SET sobra_kg = sobra_kg + ? WHERE carne = ?')
    valores = (dados.quantidade, dados.carne)
    cursor.execute(comando, valores)
    conexao.commit()
    conexao.close()
    return {'status': 'sucesso', 'msg': f'{dados.quantidade} kg adicionados a {dados.carne}'}
    

@app.post('/reset')
def reset():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT carne, usado_kg, sobra_kg FROM estoque_carnes')
    dados = cursor.fetchall()
    with open(f'backup-{date.today()}.txt', 'w', encoding='UTF-8') as backup:
        for carne, usado, sobra in dados:
            if usado != 0.0 or sobra != 0.0:
                backup.write(f'{carne}: usado_kg {usado} --- sobra_kg {sobra}\n')
    cursor.execute('UPDATE estoque_carnes SET usado_kg = 0.0, sobra_kg = 0.0')
    conexao.commit()
    conexao.close()
    return {'status': 'sucesso', 'msg': 'dados resetados, backup salvo'}







