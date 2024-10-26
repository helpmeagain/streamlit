import streamlit as st
import plotly.express as px

def line_chart(data, coluna_data, titulo, filtro_data='2021-01-01'):
    data_filtrada = data[data[coluna_data] >= filtro_data]
    dados_agrupados = data_filtrada.groupby(coluna_data).size().reset_index(name='quantidade')
    
    st.subheader(titulo, divider=False)
    fig = px.line(
        dados_agrupados, 
        x=coluna_data, 
        y='quantidade', 
        markers=True, 
        labels={coluna_data: titulo, "quantidade": "Quantidade"}
    )
    st.plotly_chart(fig)
