import streamlit as st
import numpy as np
from PIL import Image
import cv2
from functions.sidebar import sidebar_and_grid
from functions.process_answer_sheet import process_answer_sheet

st.title("Como é detectado as questões do gabarito?")
gabarito = st.file_uploader("Escolha uma imagem do gabarito", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if gabarito is not None:
    image = Image.open(gabarito)
    image_np = np.array(image)

    with st.sidebar:
        num_questions, num_choices, question_spacing, choice_spacing, circle_radius = sidebar_and_grid(image_np)

    marked_image, red_circles_image, answers = process_answer_sheet(
        image_np,
        num_questions,
        num_choices,
        question_spacing,
        choice_spacing,
        circle_radius
    )

    marked_image_rgb = cv2.cvtColor(marked_image, cv2.COLOR_BGR2RGB)
    red_circles_image_rgb = cv2.cvtColor(red_circles_image, cv2.COLOR_BGR2RGB)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(image, caption="Imagem Original", width=200)
    with col2:
        st.image(marked_image_rgb, caption="Imagem com Círculos Detectados", width=200)
    with col3:
        st.image(red_circles_image_rgb, caption="Imagem com Respostas Corretas em Vermelho", width=200)

    st.write(answers)
