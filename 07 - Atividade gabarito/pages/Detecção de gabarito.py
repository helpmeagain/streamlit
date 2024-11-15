import streamlit as st
from PIL import Image
import cv2
import numpy as np
import pandas as pd
import plotly.express as px
from functions.process_answer_sheet import process_answer_sheet
from functions.sidebar import sidebar_and_grid

st.title("Detecção de Questões Marcadas e Estatísticas")

gabarito_resposta = st.file_uploader("Escolha o gabarito resposta", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
gabarito_alunos = st.file_uploader("Escolha os gabaritos dos alunos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if gabarito_resposta is not None and gabarito_alunos is not None:
    gabarito_image = Image.open(gabarito_resposta)
    gabarito_np = np.array(gabarito_image)
    
    with st.sidebar:
        num_questions, num_choices, question_spacing, choice_spacing, circle_radius = sidebar_and_grid(gabarito_np)

    _, _, gabarito_answers = process_answer_sheet(
        gabarito_np,
        num_questions,
        num_choices,
        question_spacing,
        choice_spacing,
        circle_radius
    )

    gabarito_dict = dict(zip(gabarito_answers["Questão"], gabarito_answers["Alternativa Marcada"]))
    acertos_por_questao = {questao: 0 for questao in gabarito_dict.keys()}
    notas_sala = []

    for aluno_gabarito in gabarito_alunos:
        aluno_image = Image.open(aluno_gabarito)
        aluno_np = np.array(aluno_image)

        _, red_circles_image, aluno_answers = process_answer_sheet(
            aluno_np,
            num_questions,
            num_choices,
            question_spacing,
            choice_spacing,
            circle_radius
        )

        aluno_answers["Correção"] = aluno_answers.apply(
            lambda row: "Correto" if gabarito_dict.get(row["Questão"]) == row["Alternativa Marcada"] else "Errado",
            axis=1
        )

        nota = aluno_answers["Correção"].value_counts().get("Correto", 0)
        aluno_answers["Nota"] = nota

        notas_sala.append({"Aluno": aluno_gabarito.name, "Nota": nota})

        for _, row in aluno_answers.iterrows():
            if row["Correção"] == "Correto":
                acertos_por_questao[row["Questão"]] += 1

        red_circles_image_rgb = cv2.cvtColor(red_circles_image, cv2.COLOR_BGR2RGB)

        st.subheader(f"Gabarito do Aluno: {aluno_gabarito.name}")
        st.write(f"**Nota Geral: {nota} / {num_questions}**")
        col1, col2 = st.columns(2)
        with col1:
            aluno_answers_without_nota = aluno_answers.drop(columns=["Nota"])
            st.dataframe(aluno_answers_without_nota.reset_index(drop=True))
        with col2:
            st.image(red_circles_image_rgb, width=310)

    acertos_df = pd.DataFrame({
        "Questão": list(acertos_por_questao.keys()),
        "Acertos": list(acertos_por_questao.values())
    })

    st.subheader("Estatísticas de Acertos por Questão")
    fig_acertos = px.line(acertos_df, x="Questão", y="Acertos", title="Número de Acertos por Questão", markers=True)

    max_acertos = max(acertos_por_questao.values())
    fig_acertos.update_layout(
        yaxis=dict(
            tickmode="linear",
            tick0=0,
            dtick=1,
            range=[0, max_acertos + 1],
        )
    )
    st.plotly_chart(fig_acertos)

    notas_df = pd.DataFrame(notas_sala)

    notas_distribuicao = notas_df["Nota"].value_counts().reset_index()
    notas_distribuicao.columns = ["Nota", "Quantidade"]
    notas_distribuicao = notas_distribuicao.sort_values("Nota")

    st.subheader("Distribuição de Notas da Sala")
    fig_notas = px.bar(
        notas_distribuicao,
        x="Nota",
        y="Quantidade",
        title="Distribuição de Notas",
        text="Quantidade",
        labels={"Quantidade": "Número de Alunos", "Nota": "Nota"}
    )

    max_quantidade = max(notas_distribuicao["Quantidade"])
    fig_notas.update_layout(
        yaxis=dict(
            tickmode="linear",
            tick0=0,
            dtick=1,
            range=[0, max_quantidade + 1],
        )
    )
    st.plotly_chart(fig_notas)
