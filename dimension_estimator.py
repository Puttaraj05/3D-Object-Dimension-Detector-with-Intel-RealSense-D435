import numpy as np
import json
import csv

class DimensionEstimator:
    def __init__(self, intrinsics, depth_scale):
        self.intrinsics = intrinsics
        self.depth_scale = depth_scale

    def pixel_to_point(self, x, y, depth):
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
        roi_depth = depth_image[y:y+h, x:x+w] * self.depth_scale
        # Outlier rejection: keep only depths within ±10% of median
        all_valid = roi_depth[roi_depth > 0]
        if all_valid.size == 0:
            return None, None, None
        median = np.median(all_valid)
        depths = all_valid[(all_valid > median * 0.9) & (all_valid < median * 1.1)]
        if depths.size == 0:
            return None, None, None
        median_depth = np.median(depths)
        # Floor modeling: take a strip at the top of the image as the floor
        floor_strip = depth_image[0:50, :] * self.depth_scale
        floor_valid = floor_strip[floor_strip > 0]
        if floor_valid.size == 0:
            return None, None, None
        floor_depth = np.median(floor_valid)
        # Get real-world coordinates for corners
        top_left = self.pixel_to_point(x, y, median_depth)
        top_right = self.pixel_to_point(x + w, y, median_depth)
        bottom_left = self.pixel_to_point(x, y + h, median_depth)
        length = np.linalg.norm(top_right - top_left)
        width = np.linalg.norm(bottom_left - top_left)
        # Height: difference between floor and object median depth
        height = floor_depth - median_depth
        # Convert to centimeters
        return length * 100, width * 100, height * 100

    def export_to_csv(self, filename, dimensions):
        length, width, height = dimensions
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Length_cm', 'Width_cm', 'Height_cm'])
            writer.writerow([length, width, height])

    def export_to_json(self, filename, dimensions):
        length, width, height = dimensions
        data = {'Length_cm': length, 'Width_cm': width, 'Height_cm': height}
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2) 