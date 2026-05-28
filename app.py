import streamlit as st
import requests
from datetime import date
dados_json = requests.get('http://127.0.0.1:8000/estoque')
dados = dados_json.json()
st.set_page_config(page_title='Estoque Açougue', page_icon='🥩')
st.title('Anotações de carnes diárias')
st.write('Estoque atual')
carnes_usadas = []
for carne, info in dados.items():
    if info['usado_kg'] > 0 or info['sobra_kg'] > 0:
        carnes_usadas.append({
            'Carne': carne,
            'Usado': f'{info['usado_kg']:.2f}',
            'Sobra': f'{info['sobra_kg']:.2f}'
        })
if len(carnes_usadas) > 0:
    st.table(carnes_usadas)
else:
    st.write('Nenhuma carne adicionada')

carne_escolhida = st.selectbox('Selecione a carne:', list(dados.keys()))
quantidade = st.number_input('Quatidade usada(kg):', min_value= 0.0, step= 0.01)
colb1, colb2, colb3 = st.columns(3)

with colb1:
    if st.button('Registrar uso'):
        pacote = {'carne': carne_escolhida, 'quantidade': quantidade}
        resposta = requests.post('http://127.0.0.1:8000/uso', json=pacote)  
        st.rerun()
with colb2:
    if st.button('Registre a sobra'):
        pacote = {'carne': carne_escolhida, 'quantidade': quantidade}
        resposta = requests.post('http://127.0.0.1:8000/sobra', json=pacote)
        st.rerun()
with colb3:
    def reset():
        resposta = requests.post('http://127.0.0.1:8000/reset')
        st.rerun()
        return resposta.content
    st.download_button(label='🚨Resetar turno e salvar', data=reset, file_name=f'Backup-{date.today()}.txt', mime='text/plain')




