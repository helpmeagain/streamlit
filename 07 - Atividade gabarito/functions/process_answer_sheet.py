# functions/process_answer_sheet.py

import cv2
import numpy as np
import pandas as pd

def process_answer_sheet(image_np, num_questions, num_choices, question_spacing, choice_spacing, circle_radius):
    # Converte para escala de cinza
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    
    # Aplica um blur para suavizar
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detecta círculos usando HoughCircles
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=5,
        maxRadius=20
    )

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

    # Imagem para marcação dos círculos detectados
    marked_image = image_np.copy()
    if circles is not None:
        for (x, y, r) in circles:
            cv2.circle(marked_image, (x, y), r, (0, 255, 0), 4)

    # Detecta as alternativas marcadas
    from functions.detect_alternatives import detect_alternatives
    marked_answers = detect_alternatives(
        circles,
        image_np,
        num_questions,
        num_choices,
        question_spacing,
        choice_spacing
    )

    # Cria tabela de respostas
    answers = pd.DataFrame(marked_answers, columns=["Questão", "Alternativa Marcada"])

    # Imagem para marcar respostas corretas
    red_circles_image = image_np.copy()
    for question_number, answer in marked_answers:
        # Calcula os índices com base nas respostas detectadas
        question_idx = int(question_number.split()[1]) - 1  # Exemplo: "Questão 1" -> índice 0
        choice_idx = ord(answer) - 65  # 'A' -> 0, 'B' -> 1, etc.

        # Calcula as coordenadas aproximadas
        choice_x = 55 + (choice_idx * choice_spacing)
        choice_y = (question_idx * question_spacing + (question_idx + 1) * question_spacing) // 2

        # Desenha o círculo vermelho
        cv2.circle(red_circles_image, (choice_x, choice_y), circle_radius, (0, 0, 255), 4)

    return marked_image, red_circles_image, answers
