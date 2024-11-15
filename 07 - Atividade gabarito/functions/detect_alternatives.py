import streamlit as st
import numpy as np
import cv2

def detect_alternatives(circles, image_np, num_questions, num_choices, question_spacing, choice_spacing):
    marked_answers = []
    
    # Tamanho fixo das alternativas e questões, ajustado pela interface
    for question_number in range(num_questions):
        # Calculando a posição de cada alternativa
        question_start_y = question_number * question_spacing
        question_end_y = question_start_y + question_spacing
        question_answers = []
        
        # Define a posição das alternativas (A, B, C, D) na linha
        for choice_number in range(num_choices):
            choice_x = 50 + (choice_number * choice_spacing)  # Deslocamento horizontal
            choice_y = (question_start_y + question_end_y) // 2  # Deslocamento vertical
            
            # Verifica se algum círculo foi detectado dentro da área da alternativa
            for circle in circles:
                x, y, r = circle
                if abs(x - choice_x) <= r and abs(y - choice_y) <= r:
                    # Verificar se a área dentro do círculo é preta (pintada de preto)
                    mask = np.zeros(image_np.shape[:2], dtype=np.uint8)
                    cv2.circle(mask, (x, y), r, 255, thickness=-1)
                    masked_area = cv2.bitwise_and(image_np, image_np, mask=mask)
                    # Verifica a média da cor na região do círculo
                    mean_color = np.mean(masked_area[mask == 255])
                    if mean_color < 50:  # Ajuste o valor de limiar conforme necessário
                        question_answers.append(chr(65 + choice_number))  # A, B, C, D
                        break

        # Se encontrou uma alternativa marcada, adiciona à lista
        if question_answers:
            marked_answers.append((f"Questão {question_number + 1}", question_answers[0]))  # Marca a primeira alternativa detectada
    
    return marked_answers