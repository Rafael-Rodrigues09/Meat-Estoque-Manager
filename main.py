import json
from datetime import datetime, date

def carregar_estoque():
    with open('estoque.json', 'r') as estoque:
        return json.load(estoque)


def salvar_estoque(dados):
    with open('estoque.json', 'w') as estoque:
        json.dump(dados, estoque)

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
    with open('estoque.json', 'w') as estoque:
        json.dump(dados, estoque)

if __name__ == '__main__':
    dados = carregar_estoque()
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