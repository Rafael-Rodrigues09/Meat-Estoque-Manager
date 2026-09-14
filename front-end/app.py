import streamlit as st
import requests
from datetime import date
from dotenv import load_dotenv
import os
import time
import pandas as pd

st.set_page_config(page_title='Estoque Açougue', page_icon='🥩')

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
API_ACESS = {'x-token': API_TOKEN}
API_URL = os.getenv('API_URL')
USER_PASS = os.getenv('USER_PASS')
ADMIN_PASS = os.getenv('ADMIN_PASS')
STORAGE_PASS = os.getenv('STORAGE_PASS')
if not 'logged' in st.session_state:
    st.session_state['logged'] = False
if st.session_state['logged'] == False:
    digited_pass = st.text_input(label='Digite a senha do banco', type='password')
    if st.button('Entrar'):
        if digited_pass == USER_PASS:
            st.session_state['logged'] = True
            st.session_state['screen'] = 'add_tab'
            st.rerun()
        elif digited_pass == ADMIN_PASS:
            st.session_state['logged'] = True
            st.session_state['screen'] = 'history_tab'
            st.rerun()
        elif digited_pass == STORAGE_PASS:
            st.session_state['logged'] = True
            st.session_state['screen'] = 'storage_tab'
            st.rerun()
        else:
            st.error('Senha incorreta')
    st.stop()
def screen_add_meats():    
    try:
        response = requests.get(f'{API_URL}/estoque', headers=API_ACESS)
        if response.status_code == 200: data = response.json()
        else:
            st.warning('API DESLIGADA. LIGUE A API COM O SEGUINTE LINK E DEPOIS REINICIE O SITE: https://nativas-grill-estoque-manager.onrender.com/')
            st.stop()
    except:
        st.warning('NÃO FOI POSSÍVEL ACESSAR O SERVIDOR.')
        st.stop()
    st.title('Anotações de carnes diárias')
    usage_meats = []
    for meat, value in data.items():
        if value['usage_kg'] > 0 or value['rest_kg'] > 0:
            usage_meats.append({
                'Carne': meat,
                'Usado': f'{value["usage_kg"]:.3f}',
                'Sobra': f'{value["rest_kg"]:.3f}'
            })
    if len(usage_meats) > 0:
        st.table(usage_meats)
    else:
        st.write('Nenhuma carne adicionada')

    meat_name = st.selectbox('Selecione a carne:', list(data.keys()), key='select_meat')
    value = st.number_input('Quatidade usada(kg):', min_value= 0.0, step= 0.01, format='%.3f')
    colb1, colb2, colb3, colb4, colb5 = st.columns(5)

    with colb1:
        if st.button('Registrar uso'):
            package = {'name': meat_name, 'value': value}
            if value > 0:
                response = requests.post(f'{API_URL}/uso', json=package, headers=API_ACESS)
                st.rerun()
            else:
                st.error('Digite um valor maior que 0')
    with colb2:
        if st.button('Registre a sobra'):
            package = {'name': meat_name, 'value': value}
            if value > 0:
                response = requests.post(f'{API_URL}/sobra', json=package, headers=API_ACESS)
                st.rerun()
            else:
                st.error('Digite um valor maior que 0')

    @st.dialog('🚨 Tem certeza que deseja RESETAR o banco e salvar como PDF? 🚨')
    def warning():    
        colw1, colw2 = st.columns(2)
        with colw1:
            if st.download_button(label='🚨SIM', data=reset, file_name=f'Backup-{date.today()}.pdf', mime='application/pdf'): st.rerun()
        with colw2:
            if st.button('NÃO'): st.rerun()

    def reset():
            response = requests.post(f'{API_URL}/reset', headers=API_ACESS)
            return response.content
    with colb3:
        if st.button('🚨 RESETAR E SALVAR'):
            warning()
            
    with colb4:
        if st.button('⟳ Reverter valor'):
            response = requests.post(f'{API_URL}/reverse', headers=API_ACESS)
            st.rerun()
    with colb5:
        if st.button('sair'):
            st.session_state['logged'] = False
            st.rerun()

def screen_history_tab():
    try:
        response = requests.get(f'{API_URL}/historico', headers=API_ACESS)
        if response.status_code == 200:
            data = response.json()
        else:
            st.warning('API DESLIGADA. LIGUE A API COM O SEGUINTE LINK E DEPOIS REINICIE O SITE: https://nativas-grill-estoque-manager.onrender.com/')
            st.stop()    
    except:
        st.warning('NÃO FOI POSSÍVEL ACESSAR O SERVIDOR')
        st.stop()        
        
    st.title('Histórico de carnes')
    if data:
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'], utc=True).dt.tz_convert('America/Cuiaba').dt.strftime('%d/%m/%Y | %H: %M')
        st.dataframe(df)
        
    else:
        st.info('Nada no histórico no momento')
        
    if st.button('sair'):
        st.session_state['logged'] = False
        st.rerun()   
def screen_storage():
    try:
        response_storage = requests.get(f'{API_URL}/allestoque', headers=API_ACESS)
        response_products = requests.get(f'{API_URL}/estoque', headers=API_ACESS)
        if response_storage.status_code == 200: data = response_storage.json()
        else:
            st.warning('API DESLIGADA. LIGUE A API COM O SEGUINTE LINK E DEPOIS REINICIE O SITE: https://nativas-grill-estoque-manager.onrender.com/')
            st.stop()
        if response_products.status_code == 200: products = response_products.json()
        else: 
            st.warning('Sem produtos')
    except:
        st.warning('Não foi possivel acessar o servidor')
    st.title('Estoque')
    if not data: st.info('Nada no estoque no momento')
    else:
        df = pd.DataFrame(data)
        df['entry_date'] = pd.to_datetime(df['entry_date'], utc=True).dt.tz_convert('America/Cuiaba').dt.strftime('%d/%m/%Y | %H: %M')
        st.dataframe(df)
        st.title('Adicionar produtos ao estoque')
        selected_product = st.selectbox('Escolha o produto', [product for product in products], key='selected_product')
        value = st.number_input('Quantidade (KG, QTD)')
        expiration_date = st.date_input('Digite a data de validade(ano/mês/dia)')
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Adicionar'): 
                if value > 0:
                    response = requests.post(f'{API_URL}/add-estoque', json={'name': selected_product, 'value': value, 'expiration_date': str(expiration_date)}, headers=API_ACESS)
                    st.rerun()
                else:
                    st.warning('Digite um valor valido')
        with col2:
            if st.button('voltar'): 
                st.session_state['logged'] = False 
                st.rerun()
if st.session_state['screen'] == 'add_tab':
    screen_add_meats()

elif st.session_state['screen'] == 'history_tab':
    screen_history_tab()

elif st.session_state['screen'] == 'storage_tab':
    screen_storage()




