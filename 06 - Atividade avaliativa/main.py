# https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2023
# https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2024
import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing import load_and_process_data
from filters import apply_filters

st.title(":green[Dashboard] - dados gripais 🦠😷")
st.write("Análise dos dados de notificações de síndrome gripal do dataSUS. " + 
    "Para fazer a análise e fazer com que os gráficos apareçam, faça o upload dos arquivos CSV com os dados de 2023 e 2024. " +
    "" )
st.write("Faça o download dos dados de [2023](https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2023) " +
    " e de [2024](https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2024).")

col1, col2 = st.columns(2)
with col1:
    csv_2023_file = st.file_uploader('Dados gripais de :green[2023]', type=['csv'])
with col2:
    csv_2024_file = st.file_uploader('Dados gripais de :green[2024]', type=['csv'])

if csv_2023_file is not None and csv_2024_file is not None:
    combined_data, data_2023, data_2024 = load_and_process_data(csv_2023_file, csv_2024_file)
    data_filtered = apply_filters(combined_data)

    st.header("Prévia dos dados", divider="green")
    st.write("Os *cinco primeiros* registros dos dados de 2023 e 2024.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dados de 2023", divider=False)
        st.write(data_2023.head())
        st.write("Total de registros: ", data_2023.shape[0])
    with col2:
        st.subheader("Dados de 2024", divider=False)
        st.write(data_2024.head())
        st.write("Total de registros: ", data_2024.shape[0])
    
    st.header("Gráficos dos dados combinados", divider="green")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribuição de etnia", divider=False)
        dados_etnia = px.pie(data_filtered[data_filtered['racaCor'].notna()], names="racaCor", hole=0.5)
        st.plotly_chart(dados_etnia)
    with col2:
        st.subheader("Distribuição de gênero", divider=False)
        dados_genero = px.pie(data_filtered, names="sexo", hole=0.5)
        st.plotly_chart(dados_genero) 

    sintomas_explodidos = data_filtered.explode('sintomas')
    sintomas_contagem = sintomas_explodidos['sintomas'].value_counts().reset_index()
    sintomas_contagem.columns = ['sintoma', 'contagem'] 

    st.subheader("Quantidade de Sintomas", divider=False)
    fig = px.bar(sintomas_contagem, x='sintoma', y='contagem', text='contagem')
    st.plotly_chart(fig) 

    data_filtered = data_filtered[data_filtered['dataInicioSintomas'] >= '2021-01-01']
    sintomas_por_data = data_filtered.groupby('dataInicioSintomas').size().reset_index(name='quantidade')

    st.subheader("Inícios de Sintomas ao Longo do Tempo", divider=False)
    fig = px.line(
        sintomas_por_data, 
        x='dataInicioSintomas', 
        y='quantidade', markers=True, 
        labels={'dataInicioSintomas': 'Data de Início dos Sintomas'}
    )
    st.plotly_chart(fig)
