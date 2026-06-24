import streamlit as st
import requests
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
api_acess = {'x-token': API_TOKEN}
API_URL = os.getenv('API_URL')
try:
    resposta = requests.get(f'{API_URL}/estoque', headers=api_acess)
    if resposta.status_code == 200:
        dados = resposta.json()
    else:
        st.warning('API DESLIGADA. LIGUE A API COM O SEGUINTE LINK E DEPOIS REINICIE O SITE: https://nativas-grill-estoque-manager.onrender.com/')
        st.stop()
except:
    st.warning('NÃO FOI POSSIVEL ACESSAR O SERVIDOR.')
    st.stop()
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

carne_nome = st.selectbox('Selecione a carne:', list(dados.keys()))
valor = st.number_input('Quatidade usada(kg):', min_value= 0.0, step= 0.01, format='%.2f')
colb1, colb2, colb3 = st.columns(3)

with colb1:
    if st.button('Registrar uso'):
        pacote = {'carne_nome': carne_nome, 'valor': valor}
        if valor > 0:
            resposta = requests.post(f'{API_URL}/uso', json=pacote, headers=api_acess)  
            st.rerun()
        else:
            st.error('Digite um valor maior que 0')
with colb2:
    if st.button('Registre a sobra'):
        pacote = {'carne_nome': carne_nome, 'valor': valor}
        if valor > 0:
            resposta = requests.post(f'{API_URL}/sobra', json=pacote, headers=api_acess)
            st.rerun()
        else:
            st.error('Digite um valor maior que 0')
with colb3:
    def reset():
        resposta = requests.post(f'{API_URL}/reset', headers=api_acess)
        st.rerun()
        return resposta.content
    st.download_button(label='🚨Resetar turno e salvar', data=reset, file_name=f'Backup-{date.today()}.txt', mime='text/plain')




