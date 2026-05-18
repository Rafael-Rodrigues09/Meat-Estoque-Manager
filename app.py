import streamlit as st
import json
from main import carregar_estoque, salvar_estoque, backup_reset

dados = carregar_estoque()

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
        dados[carne_escolhida]['usado_kg'] += quantidade
        salvar_estoque(dados)
        st.success(f'{carne_escolhida} registrado: {quantidade} kg adicionados')
        st.rerun()
with colb2:
    if st.button('Registre a sobra'):
        dados[carne_escolhida]['sobra_kg'] += quantidade
        salvar_estoque(dados)
        st.success(f'{carne_escolhida} registrado: {quantidade} kg adicionados')
        st.rerun()
with colb3:
    if st.button('🚨 Resetar turno e salvar'):
        backup_reset(dados)
        st.success('Dados resetados e salvos')
        st.rerun()


