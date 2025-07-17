import cv2
import time

class Visualizer:
    def __init__(self):
        self.last_time = time.time()
        self.fps = 0

    def update_fps(self):
        now = time.time()
        dt = now - self.last_time
        self.fps = 1.0 / dt if dt > 0 else 0
        self.last_time = now
        return self.fps

    def draw(self, frame, bbox=None, dimensions=None, contour=None):
        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if contour is not None:
            cv2.drawContours(frame, [contour], -1, (255, 0, 0), 2)
        if dimensions:
            length, width, height = dimensions
            text = f"L: {length:.1f}cm  W: {width:.1f}cm  H: {height:.1f}cm"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        fps = self.update_fps()
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return frame 