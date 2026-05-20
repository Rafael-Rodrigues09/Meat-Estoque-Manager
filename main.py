import sqlite3
from datetime import datetime, date

def carregar_estoque():
    dados = {}
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT carne, usado_kg, sobra_kg FROM estoque_carnes')
    banco = cursor.fetchall()
    for carne, usado, sobra in banco:
        dados[carne] = {'usado_kg': usado, 'sobra_kg': sobra}
    conexao.close()
    return dados


def salvar_estoque(dados):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    for carne, info in dados.items():
        comando = 'UPDATE estoque_carnes SET usado_kg = ?, sobra_kg = ? WHERE carne = ?'
        valores = (info['usado_kg'], info['sobra_kg'], carne)
        cursor.execute(comando, valores)
    conexao.commit()
    conexao.close()

def gerar_relatorio(dados):
    contador = 0
    print('\n--------- RELATORIO TURNO ---------')
    for carne, info in dados.items():
        if info['usado_kg'] != 0.0 or info['sobra_kg'] != 0.0:
            print(f'{carne}: {info['usado_kg']} kg USADOS ------------- {info['sobra_kg']} kg SOBRADOS')
            contador += 1
    if contador == 0:
        print('Nenhuma carne adicionada')

def backup_reset(dados):
    with open(f'backup {date.today()}.txt', 'w', encoding='utf-8') as backup:
        for carne, info in dados.items():
            if info['usado_kg'] != 0.0 or info['sobra_kg'] != 0.0:
                backup.write(f'{carne}: {info['usado_kg']:.2f} kg USADOS ----------- {info['sobra_kg']:.2f} kg SOBRADOS\n')
    for carne, info in dados.items():
        info['usado_kg'] = 0.0
        info['sobra_kg'] = 0.0
    salvar_estoque(dados)

def inicializar_banco():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS estoque_carnes(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    resultado = cursor.fetchall()
    if resultado[0][0] == 0:
        add_carnes = 'INSERT INTO estoque_carnes (carne, usado_kg, sobra_kg   ) VALUES (?, ?, ?)'
        cursor.executemany(add_carnes, lista_carnes)         
                
    conexao.commit()
    conexao.close()

if __name__ == '__main__':
    dados = carregar_estoque()
    print (dados)
    one_zero_carne = True
    one_zero_sobra = True
    while one_zero_carne:
        carne = input('Digite a carne que deseja adicionar (Para encerrar digite FIM. Para a sobra de carnes digite SOBRA): ').upper()

        if carne == 'FIM':
            reset_or_not = input('Deseja apenas salvar? (digite -> 0). Deseja resetar e salvar o dia? (digite -> 1): ')
            if reset_or_not == '0':
                gerar_relatorio(dados)
                print('Dados salvos!')
                one_zero_carne = False
            elif reset_or_not == '1':
                gerar_relatorio(dados)
                backup_reset(dados)
                print('Reset completo, arquivo de backup salvo')
                one_zero_carne = False

            
        elif carne == 'SOBRA':
            while one_zero_sobra:
                sobra_input = input('Digite a carne da sobra (Para encerrar digite FIM. Para voltar sem salvar para adição de carnes digite ADD): ').upper()
                if sobra_input == 'FIM':
                    reset_or_not = input('Deseja apenas salvar? (digite -> 0). Deseja resetar e salvar o dia? (digite -> 1): ')
                    if reset_or_not == '0':
                        gerar_relatorio(dados)
                        print('Dados salvos!')
                        one_zero_carne = False
                        break
                    elif reset_or_not == '1':
                        gerar_relatorio(dados)
                        backup_reset(dados)
                        print('Reset completo, arquivo de backup salvo')
                        one_zero_carne = False
                        break
                elif sobra_input == 'ADD':
                    break
                if sobra_input in dados:
                    try:
                        sobra_qtd = float(input('Digite quanto sobrou: '))
                        dados[sobra_input]['sobra_kg'] += sobra_qtd
                        print(f'{sobra_qtd} kg de SOBRA adicionado a {sobra_input}')
                    except:
                        print('Digite o peso válido')
                else:
                    print('Digite uma carne válida')
            

                
        elif carne in dados:
            try:
                usado = float(input('Quanto usou?: '))
                dados[carne]['usado_kg'] += usado
                print(f'{dados[carne]['usado_kg']} kg Adicionado a {carne}')
            except:
                print('Digite uma carne ou peso válidos')
        else:
            print('Digite uma carne válida')
    salvar_estoque(dados)