import cv2

def read_bubble(thresh, x, y, w, h):
    """
    Returns fill ratio of a bubble region
    """
    roi = thresh[y:y+h, x:x+w]
    filled = cv2.countNonZero(roi)
    total = w * h
    return filled / total if total > 0 else 0


def grade_from_template(thresh, template, answer_key, threshold=0.35):
    """
    Grades an OMR sheet using a fixed template.

    Args:
        thresh: thresholded OMR image
        template: template JSON loaded as dict
        answer_key: dict {question: correct_option}
        threshold: fill threshold

    Returns:
        results (list of dicts), total_correct (int)
    """

    results = []
    total_correct = 0

    for paper_name, questions in template.items():
        for q_no, options in questions.items():

            fill_values = {}

            # Read each option bubble
            for option, (x, y, w, h) in options.items():
                fill_values[option] = read_bubble(thresh, x, y, w, h)

            # Determine marked option
            marked = None
            max_fill = max(fill_values.values())

            if max_fill >= threshold:
                # Check multi-mark
                marked_options = [
                    opt for opt, val in fill_values.items()
                    if val >= threshold
                ]
                if len(marked_options) == 1:
                    marked = marked_options[0]
                else:
                    marked = "INVALID"

            correct_answer = answer_key.get(int(q_no))
            is_correct = marked == correct_answer

            if is_correct:
                total_correct += 1

            results.append({
                "paper": paper_name,
                "question": int(q_no),
                "marked": marked,
                "answer": correct_answer,
                "correct": is_correct,
                "confidence": round(max_fill, 3)
            })

    return results, total_correct
