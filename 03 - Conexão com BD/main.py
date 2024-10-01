import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Inicializa conexão com BD
conn = st.connection('mysql', type='sql')

# Carrega dados do BD
df = conn.query('SELECT * FROM actor;', ttl=600)

#Título da aplicação
st.title('Análise de Dados dos Atores')

#Exibir tabela de dados
st.subheader('Tabela de atores')
st.dataframe(df)

