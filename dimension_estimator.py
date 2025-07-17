import numpy as np

class DimensionEstimator:
    def __init__(self, intrinsics, depth_scale):
        self.intrinsics = intrinsics
        self.depth_scale = depth_scale

    def pixel_to_point(self, x, y, depth):
        # Convert pixel (x, y) and depth to real-world coordinates (in meters)
        fx = self.intrinsics.fx
        fy = self.intrinsics.fy
        ppx = self.intrinsics.ppx
        ppy = self.intrinsics.ppy
        X = (x - ppx) / fx * depth
        Y = (y - ppy) / fy * depth
        Z = depth
        return np.array([X, Y, Z])

    def estimate_dimensions(self, bbox, contour, depth_image):
        x, y, w, h = bbox
        # Get depth values within the bounding box
        roi_depth = depth_image[y:y+h, x:x+w] * self.depth_scale
        # Mask out zero depth (invalid)
        valid_depths = roi_depth[roi_depth > 0]
        if valid_depths.size == 0:
            return None, None, None
        median_depth = np.median(valid_depths)
        # Get real-world coordinates for corners
        top_left = self.pixel_to_point(x, y, median_depth)
        top_right = self.pixel_to_point(x + w, y, median_depth)
        bottom_left = self.pixel_to_point(x, y + h, median_depth)
        # Length (X axis): distance between top_left and top_right
        length = np.linalg.norm(top_right - top_left)
        # Width (Y axis): distance between top_left and bottom_left
        width = np.linalg.norm(bottom_left - top_left)
        # Height (Z axis): max depth in ROI minus min depth (object height)
        height = np.percentile(valid_depths, 95) - np.percentile(valid_depths, 5)
        # Convert to centimeters
        return length * 100, width * 100, height * 100 