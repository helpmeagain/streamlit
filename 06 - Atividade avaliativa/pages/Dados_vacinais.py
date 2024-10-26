import streamlit as st
import pandas as pd
from data_processing import load_and_process_data
from charts.pie_chart import pie_chart
import plotly.express as px

st.title(":red[Dashboard] - dados vacinais 💉👩‍⚕️")
st.write("Análise dos dados de vacinações sob síndrome gripal do dataSUS. " + 
    "Para fazer a análise e fazer com que os gráficos apareçam, faça o upload dos arquivos CSV com os dados de 2023 e 2024. " +
    "" )
st.write("Faça o download dos dados de [2023](https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2023) " +
    " e de [2024](https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2024).")

col1, col2 = st.columns(2)
with col1:
    csv_2023_file = st.file_uploader('Dados gripais de :red[2023]', type=['csv'])
with col2:
    csv_2024_file = st.file_uploader('Dados gripais de :red[2024]', type=['csv'])

if csv_2023_file is not None and csv_2024_file is not None:
    combined_data, data_2023, data_2024 = load_and_process_data(csv_2023_file, csv_2024_file)

    st.header("Prévia dos dados", divider="red")
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

    st.header("Dados vacinais", divider="red")
    st.subheader("Comparação de vacinação entre 2023 e 2024", divider=False)
    data_2023['Ano'] = '2023'
    data_2024['Ano'] = '2024'

    label_map = {1: 'Sim', 2: 'Não', 3: 'Ignorado'}
    combined_data_vacina = pd.concat([data_2023[['codigoRecebeuVacina', 'Ano']], data_2024[['codigoRecebeuVacina', 'Ano']]])
    combined_data_vacina['codigoRecebeuVacina'] = combined_data_vacina['codigoRecebeuVacina'].map(label_map)

    fig = px.histogram(
        combined_data_vacina, 
        x='codigoRecebeuVacina', 
        color='Ano', 
        barmode='group', 
        labels={'codigoRecebeuVacina': 'Se vacinou?'}, 
        title="",
        text_auto=True,
    )

    fig.update_yaxes(title_text="Quantidade de pessoas")
    st.plotly_chart(fig, use_container_width=True)

    combined_vaccine_data = pd.concat([
        combined_data[['codigoLaboratorioPrimeiraDose']].rename(columns={'codigoLaboratorioPrimeiraDose': 'codigoLaboratorio'}),
        combined_data[['codigoLaboratorioSegundaDose']].rename(columns={'codigoLaboratorioSegundaDose': 'codigoLaboratorio'})
    ])
    combined_vaccine_data = combined_vaccine_data[combined_vaccine_data['codigoLaboratorio'].notna()]
    pie_chart(combined_vaccine_data, 'codigoLaboratorio', "Distribuição de fabricantes de vacina")

    st.header("Comparação de datas de vacinação e início de sintomas", divider="red")
   
    # Convertendo colunas de data para datetime
    combined_data['dataInicioSintomas'] = pd.to_datetime(combined_data['dataInicioSintomas'], errors='coerce')
    combined_data['dataPrimeiraDose'] = pd.to_datetime(combined_data['dataPrimeiraDose'], errors='coerce')
    combined_data['dataSegundaDose'] = pd.to_datetime(combined_data['dataSegundaDose'], errors='coerce')
    combined_data = combined_data[combined_data['dataInicioSintomas'].dt.year >= 2020]
    combined_data = combined_data[combined_data['dataPrimeiraDose'].dt.year >= 2020]
    combined_data = combined_data[combined_data['dataSegundaDose'].dt.year >= 2020]

    symptoms_count = combined_data['dataInicioSintomas'].value_counts().reset_index()
    symptoms_count.columns = ['Data', 'ContagemSintomas']
    vaccine1_count = combined_data['dataPrimeiraDose'].value_counts().reset_index()
    vaccine1_count.columns = ['Data', 'ContagemPrimeiraDose']
    vaccine2_count = combined_data['dataSegundaDose'].value_counts().reset_index()
    vaccine2_count.columns = ['Data', 'ContagemSegundaDose']

    merged_data = symptoms_count.merge(vaccine1_count, on='Data', how='outer').merge(vaccine2_count, on='Data', how='outer').fillna(0)

    fig_comparison = px.line(
        merged_data, 
        x='Data', 
        y=['ContagemSintomas', 'ContagemPrimeiraDose', 'ContagemSegundaDose'],
        labels={'value': 'Contagem', 'variable': 'Tipo'},
    )
    
    fig_comparison.update_layout(
        yaxis_title='Contagem', 
        xaxis_title='Data', 
        legend_title='Tipo',
        xaxis=dict(tickformat='%Y-%m-%d')
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)