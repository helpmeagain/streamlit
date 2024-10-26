import streamlit as st
import plotly.express as px

def pie_chart(data, coluna, titulo):
    st.subheader(titulo, divider=False)

    data_filtrada = data[data[coluna].notna()]
    grafico = px.pie(data_filtrada, names=coluna, hole=0.5)
    grafico.update_traces(hovertemplate='%{label}')
    st.plotly_chart(grafico)
