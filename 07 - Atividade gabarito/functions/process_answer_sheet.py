import cv2
import numpy as np
import pandas as pd
from collections import namedtuple
from functions.detect_alternatives import detect_alternatives

ProcessedResult = namedtuple("ProcessedResult", ["marked_image", "red_circles_image", "answers"])

def detect_circles(image, dp=1.2, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=20):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=dp,
        minDist=minDist,
        param1=param1,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius
    )
    return np.round(circles[0, :]).astype("int") if circles is not None else None


def draw_circles(image, circles, color=(0, 255, 0), thickness=4):
    if circles is not None:
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, color, thickness)


def get_choice_coordinates(question_idx, choice_idx, choice_spacing, question_spacing, offset_x=55):
    choice_x = offset_x + (choice_idx * choice_spacing)
    choice_y = (question_idx * question_spacing + (question_idx + 1) * question_spacing) // 2
    return choice_x, choice_y


def process_answer_sheet(image_np, num_questions, num_choices, question_spacing, choice_spacing, circle_radius):
    # Conversão para escala de cinza
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Detecta círculos
    circles = detect_circles(gray)
    if circles is None:
        raise ValueError("Nenhum círculo foi detectado na imagem.")

    # Imagem com círculos marcados
    marked_image = image_np.copy()
    draw_circles(marked_image, circles)

    # Detecta alternativas marcadas
    marked_answers = detect_alternatives(
        circles,
        image_np,
        num_questions,
        num_choices,
        question_spacing,
        choice_spacing
    )

    # Imagem com respostas corretas destacadas
    red_circles_image = image_np.copy()
    for question_number, answer in marked_answers:
        question_idx = int(question_number.split()[1]) - 1  # Exemplo: "Questão 1" -> índice 0
        choice_idx = ord(answer) - 65  # 'A' -> 0, 'B' -> 1, etc.
        choice_x, choice_y = get_choice_coordinates(
            question_idx, choice_idx, choice_spacing, question_spacing
        )
        cv2.circle(red_circles_image, (choice_x, choice_y), circle_radius, (0, 0, 255), 4)

    # Criação da tabela de respostas
    answers = pd.DataFrame(marked_answers, columns=["Questão", "Alternativa Marcada"])

    return ProcessedResult(marked_image, red_circles_image, answers)
