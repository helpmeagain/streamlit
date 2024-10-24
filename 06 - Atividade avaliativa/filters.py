import streamlit as st

def apply_filters(combined_data):
    st.sidebar.header("Filtros")
    
    # Filtro de Município
    municipio_filter = st.sidebar.selectbox("Selecione o município", 
        ['Todos'] + list(combined_data['municipio'].unique()), index=0)
    
    # Filtro de Estado
    estado_filter = st.sidebar.selectbox("Selecione o estado", 
        ['Todos'] + list(combined_data['estado'].unique()), index=0)

    if st.sidebar.button('Limpar todos os filtros'):
        municipio_filter = 'Todos'
        estado_filter = 'Todos'
    
    # Filtrando os dados
    if municipio_filter == 'Todos' and estado_filter == 'Todos':
        data_filtered = combined_data
    elif municipio_filter == 'Todos':
        data_filtered = combined_data[combined_data['estado'] == estado_filter]
    elif estado_filter == 'Todos':
        data_filtered = combined_data[combined_data['municipio'] == municipio_filter]
    else:
        data_filtered = combined_data[(combined_data['municipio'] == municipio_filter) & 
                                      (combined_data['estado'] == estado_filter)]
    
    return data_filtered
