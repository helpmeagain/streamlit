import streamlit as st
import pandas as pd
import plotly.express as px

csv_file = st.file_uploader('Escolha o arquivo CSV com os dados dos candidatos. É necessário inserir para mostrar os gráficos', type=['csv'])

if csv_file is not None:
    data = pd.read_csv(csv_file, encoding='ISO-8859-1', delimiter=';')

    # SIDEBAR
    st.sidebar.header("Filtros")
    unidade_eleitoral_filter = st.sidebar.selectbox("Selecione a Unidade Eleitoral (NM_UE)", data['NM_UE'].unique(), index = 0)
    cargo_filter = st.sidebar.selectbox("Selecione um Cargo (DS_CARGO)", data['DS_CARGO'].unique(), index = 0)

    if st.sidebar.button('Limpar todos os filtros'):
        unidade_eleitoral_filter = ''
        cargo_filter = ''

    data_filtered = data[(data['NM_UE'] == unidade_eleitoral_filter) & (data['DS_CARGO'] == cargo_filter)]
    if data_filtered.empty:
        st.warning("Não há dados para exibir com os filtros selecionados. Selecione outros filtros e dados irão aparecer.")
        st.stop()
    
    # TABELA PRÉVIA DE DADOS
    st.title("Prévia dos dados")
    st.write(data_filtered)

    # --- DISTRIBUIÇÃO DO GRAU DE INSTRUÇÃO --- #
    st.title("Distribuição do Grau de Instrução")

    # GRÁFICO DIST. GRAU DE INSTRUÇÃO
    st.subheader("Distribuição por Grau de Instrução", divider=False)
    dados_instrucao = data_filtered['DS_GRAU_INSTRUCAO'].value_counts()
    st.bar_chart(dados_instrucao, y='count')

    # --- DISTRIBUIÇÃO DO GRAU DE INSTRUÇÃO --- #
    st.title("Relação entre Gênero e Grau de Instrução")

    # GRÁFICO RELAÇÃO GÊNERO E INSTRUÇÃO
    st.subheader("Grau de Instrução por gênero", divider=False)
    dados_instrucao_genero = data_filtered.groupby(['DS_GRAU_INSTRUCAO', 'DS_GENERO']).size().unstack().fillna(0)
    st.bar_chart(dados_instrucao_genero, stack=False)

    # GRÁFICO ETNIA
    st.subheader("Distribuição da Cor/Raça dos Candidatos", divider=False)
    dados_etnia = px.pie(data_filtered, names="DS_COR_RACA", hole=0.5)
    st.plotly_chart(dados_etnia)

    # --- DISTRIBUIÇÃO POR GÊNERO --- #
    st.title("Distribuição por gênero")

    # GRÁFICO GÊNERO DOS CANDIDATOS
    st.subheader("Distribuição de gênero", divider=False)
    dados_genero = px.pie(data_filtered, names="DS_GENERO", hole=0.5)
    st.plotly_chart(dados_genero)

    # GRÁFICO CANDIDATAS FEMININAS
    st.subheader('Quantidade de Candidatas Femininas por Partido', divider=False)
    feminino_data_filtered = data_filtered.query('DS_GENERO == "FEMININO"')
    contagem_por_partido = feminino_data_filtered['SG_PARTIDO'].value_counts().to_frame().reset_index()
    contagem_por_partido.columns = ['SG_PARTIDO', 'count']
    dados_feminino = px.bar(
        contagem_por_partido, 
        x='SG_PARTIDO', 
        y='count', 
        color='count', 
        color_continuous_scale='Blues_r',
        labels={'count': 'Quantidade de Candidatas', 'SG_PARTIDO' : 'Sigla do partido'}
    )
    st.plotly_chart(dados_feminino)

    # GRÁFICO CANDIDATOS MASCULINOS
    st.subheader('Quantidade de Candidatos Masculinos por Partido', divider=False)
    masculino_data_filtered = data_filtered.query('DS_GENERO == "MASCULINO"')
    contagem_por_partido = masculino_data_filtered['SG_PARTIDO'].value_counts().to_frame().reset_index()
    contagem_por_partido.columns = ['SG_PARTIDO', 'count']
    dados_masculino = px.bar(
        contagem_por_partido, 
        x='SG_PARTIDO', 
        y='count', 
        color='count', 
        color_continuous_scale='Blues_r',
        labels={'count': 'Quantidade de Candidatos', 'SG_PARTIDO' : 'Sigla do partido'}
    )
    st.plotly_chart(dados_masculino)

    # GRÁFICO PROPORÇÃO MASC/FEM
    st.subheader('Proporção de Candidatos Masculinos e Femininos por Partido', divider=False)
    genero_data_filtered = data_filtered.groupby(['SG_PARTIDO', 'DS_GENERO']).size().reset_index(name='count')
    data_proporcao_genero = px.histogram(
        genero_data_filtered, 
        x='SG_PARTIDO', 
        y='count',
        color='DS_GENERO',
        labels={'count': 'Quantidade de Candidatos', 'SG_PARTIDO' : 'Sigla do partido', 'DS_GENERO': 'Gênero'}
    )
    data_proporcao_genero.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(data_proporcao_genero)

    