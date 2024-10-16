import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Carregar os dados
data = pd.read_csv("./vendas.csv", sep=";")

# Tratar variáveis
data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y", errors="coerce")
data["Total"] = data["Total"].str.replace(",", ".").astype(float)
data["Rating"] = pd.to_numeric(data["Rating"].str.replace(",", "."), errors="coerce")

# BARRA LATERAL
mes = sorted(data["Date"].dt.month.unique().astype(int))
mes = [m for m in mes if m > 0] 
mes_side_bar = st.sidebar.selectbox("Mês", mes)

# GRÁFICO FATURAMENTO POR DIA
faturamento_por_dia_cidade_e_produto = data.groupby(["Date", "City", "Product line"])["Total"].sum().reset_index()

filtrar_dados_por_mes = faturamento_por_dia_cidade_e_produto[
    faturamento_por_dia_cidade_e_produto['Date'].dt.month == mes_side_bar
]

st.title("Faturamento por dia")
grafico_por_dia = filtrar_dados_por_mes.pivot_table(
    index='Product line', 
    columns='City', 
    values='Total', 
    aggfunc='sum'
)
st.bar_chart(grafico_por_dia)


# GRÁFICO FATURAMENTO POR CIDADE
st.title("Faturamento por cidade")
grafico_por_cidade = filtrar_dados_por_mes.pivot_table(
    index='City', 
    values='Total', 
    aggfunc='sum'
)
st.bar_chart(grafico_por_cidade)

# GRÁFICO FATURAMENTO POR TIPO DE PAGAMENTO
faturamento_por_pagamento = data.groupby(["Date", 'Payment'])['Total'].sum().reset_index()
filtrar_dados_por_mes = faturamento_por_pagamento[
    faturamento_por_pagamento['Date'].dt.month == mes_side_bar
]

st.title("Faturamento por tipo de pagamento")
grafico_por_pagamento = filtrar_dados_por_mes.pivot_table(
    index='Payment', 
    values='Total', 
    aggfunc='sum'
)
fig, ax = plt.subplots()
ax.pie(grafico_por_pagamento['Total'], labels=grafico_por_pagamento.index, autopct='%1.1f%%')
st.pyplot(fig)

# GRÁFICO AVALIAÇÃO MÉDIA 
avaliacao_media_cidade = data.groupby(['City', "Date"])['Rating'].mean().reset_index()
filtrar_dados_por_mes = avaliacao_media_cidade[
    avaliacao_media_cidade['Date'].dt.month == mes_side_bar
]

st.title("Avaliação média")
grafico_por_avaliação = filtrar_dados_por_mes.pivot_table(
    index='City', 
    values='Rating', 
    aggfunc='mean'
)
st.bar_chart(grafico_por_avaliação)