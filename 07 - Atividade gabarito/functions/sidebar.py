import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import cv2
from functions.detect_alternatives import detect_alternatives

def sidebar_and_grid(image_np):
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input("Número questões", min_value=1, value=10, step=1)
    with col2:
        num_choices = st.number_input("Número alternativas", min_value=2, max_value=6, value=4, step=1)

    question_spacing = st.slider("Espaçamento entre as questões", min_value=20, max_value=60, value=30, step=1)
    choice_spacing = st.slider("Espaçamento entre as alternativas", min_value=20, max_value=100, value=54, step=1)

    grid_image = image_np.copy()
    circle_radius = 12 

    for i in range(num_questions):
        question_start_y = i * question_spacing
        question_end_y = question_start_y + question_spacing
        
        cv2.rectangle(grid_image, (35, question_start_y), (50 + (num_choices * choice_spacing), question_end_y), (0, 255, 0), 2)
        
        for j in range(num_choices):
            choice_x = 55 + (j * choice_spacing)
            choice_y = (question_start_y + question_end_y) // 2
            cv2.circle(grid_image, (choice_x, choice_y), circle_radius, (255, 0, 0), 2)

    grid_image_rgb = cv2.cvtColor(grid_image, cv2.COLOR_BGR2RGB)
    
    st.sidebar.image(grid_image_rgb, caption="Visualização do Grid", width=200)

    return num_questions, num_choices, question_spacing, choice_spacing, circle_radius
