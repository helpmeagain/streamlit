import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing import load_and_process_data
from filters import apply_filters
from charts.pie_chart import pie_chart
from charts.line_chart import line_chart

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
    
    st.header("Dados identitários da população", divider="green")
    col1, col2 = st.columns(2)
    with col1:
        pie_chart(data_filtered[data_filtered['racaCor'].notna()], 'racaCor', "Distribuição de etnia")
    with col2:
        pie_chart(data_filtered, 'sexo', "Distribuição de gênero")
    
    with col1:
        pie_chart(data_filtered, 'profissionalSaude', "Profissionais da saúde")
    with col2:
        pie_chart(data_filtered, 'profissionalSeguranca', "Profissionais da segurança")


    st.header("Dados dos sintomas", divider="green")
    sintomas_explodidos = data_filtered.explode('sintomas')
    sintomas_contagem = sintomas_explodidos['sintomas'].value_counts().reset_index()
    sintomas_contagem.columns = ['sintoma', 'contagem'] 

    st.subheader("Quantidade de Sintomas", divider=False)
    fig = px.bar(sintomas_contagem, x='sintoma', y='contagem', text='contagem')
    st.plotly_chart(fig) 

    col1, col2 = st.columns(2)
    with col1:
        line_chart(data_filtered, 'dataInicioSintomas', "Inícios dos sintomas")
    with col2: 
        line_chart(data_filtered, 'dataEncerramento', "Fim dos sintomas")

    pie_chart(data_filtered[data_filtered['classificacaoFinal'].notna()], "classificacaoFinal", "Diagnóstico")
