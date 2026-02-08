import cv2

def resize(image, width=1000):
    h, w = image.shape[:2]
    ratio = width / float(w)
    return cv2.resize(image, (width, int(h * ratio)))
