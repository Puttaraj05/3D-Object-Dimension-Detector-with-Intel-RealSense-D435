from realsense_camera import RealSenseCamera
from object_detector import ObjectDetector
from dimension_estimator import DimensionEstimator
from visualizer import Visualizer
import cv2

if __name__ == "__main__":
    try:
        with RealSenseCamera() as cam:
            detector = ObjectDetector()
            estimator = DimensionEstimator(cam.get_intrinsics(), cam.get_depth_scale())
            visualizer = Visualizer()
            while True:
                color_image, depth_image = cam.get_frames()
                if color_image is None or depth_image is None:
                    print("No frames received. Skipping...")
                    continue
                bbox, contour = detector.detect_largest_object(color_image)
                dimensions = None
                if bbox and contour is not None:
                    dimensions = estimator.estimate_dimensions(bbox, contour, depth_image)
                vis_frame = color_image.copy()
                vis_frame = visualizer.draw(vis_frame, bbox, dimensions, contour)
                cv2.imshow("3D Object Dimension Detection", vis_frame)
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
            cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error: {e}") 