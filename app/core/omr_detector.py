import cv2
import numpy as np

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    return gray, thresh

def detect_bubbles(thresh):
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    bubbles = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        ar = w / float(h)
        if 15 < w < 60 and 15 < h < 60 and 0.8 < ar < 1.2:
            bubbles.append((x, y, w, h))
    return sorted(bubbles, key=lambda b: (b[1], b[0]))

def group_bubbles(bubbles, row_tolerance=15):
    questions = []
    current = []

    for b in bubbles:
        if not current:
            current.append(b)
        elif abs(b[1] - current[-1][1]) < row_tolerance:
            current.append(b)
        else:
            questions.append(current)
            current = [b]

    if current:
        questions.append(current)

    return questions
