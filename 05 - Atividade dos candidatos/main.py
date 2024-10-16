import streamlit as st
import pandas as pd

csv_file = st.file_uploader('Escolha o arquivo CSV com os dados dos candidatos', type=['csv'])
if csv_file is not None:
    try:
        data = pd.read_csv(csv_file, encoding='ISO-8859-1', delimiter=';')
        st.title("Prévia dos dados")
        st.write(data)
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")
