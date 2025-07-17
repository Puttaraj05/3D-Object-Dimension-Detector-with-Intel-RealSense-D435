import cv2
import numpy as np

class ObjectDetector:
    def __init__(self, min_area=5000):
        self.min_area = min_area

    def detect_largest_object(self, color_image):
        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None, None
        # Find the largest contour by area
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) < self.min_area:
            return None, None
        x, y, w, h = cv2.boundingRect(largest)
        return (x, y, w, h), largest 