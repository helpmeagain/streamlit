import numpy as np
import cv2


def calculate_choice_position(question_start_y, question_end_y, choice_number, choice_spacing, offset_x=50):
    choice_x = offset_x + (choice_number * choice_spacing)
    choice_y = (question_start_y + question_end_y) // 2
    return choice_x, choice_y


def is_circle_marked(circle, choice_position, image_np, threshold=50):
    x, y, r = circle
    choice_x, choice_y = choice_position

    if abs(x - choice_x) <= r and abs(y - choice_y) <= r:
        mask = np.zeros(image_np.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (x, y), r, 255, thickness=-1)
        masked_area = cv2.bitwise_and(image_np, image_np, mask=mask)
        mean_color = np.mean(masked_area[mask == 255])
        return mean_color < threshold

    return False


def detect_alternatives(circles, image_np, num_questions, num_choices, question_spacing, choice_spacing):
    marked_answers = []

    for question_number in range(num_questions):
        question_start_y = question_number * question_spacing
        question_end_y = question_start_y + question_spacing
        question_answers = []

        for choice_number in range(num_choices):
            choice_position = calculate_choice_position(
                question_start_y, question_end_y, choice_number, choice_spacing
            )

            for circle in circles:
                if is_circle_marked(circle, choice_position, image_np):
                    question_answers.append(chr(65 + choice_number))  # 'A', 'B', 'C', ...
                    break

        if question_answers:
            marked_answers.append((f"Questão {question_number + 1}", question_answers[0]))

    return marked_answers
