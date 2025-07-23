import pyrealsense2 as rs
import numpy as np

class RealSenseCamera:
    def __init__(self, width=640, height=480, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.pipeline = None
        self.config = None
        self.profile = None
        self.depth_scale = None
        self.intrinsics = None

    def __enter__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, self.fps)
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, self.fps)
        try:
            self.profile = self.pipeline.start(self.config)
            depth_sensor = self.profile.get_device().first_depth_sensor()
            self.depth_scale = depth_sensor.get_depth_scale()
            self.intrinsics = self.profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
            # Initialize RealSense filters
            self.spatial = rs.spatial_filter()
            self.temporal = rs.temporal_filter()
        except Exception as e:
            raise RuntimeError(f"Failed to start RealSense pipeline: {e}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pipeline:
            self.pipeline.stop()

    def get_frames(self):
        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                return None, None
            # Apply spatial and temporal filters to depth frame
            depth_frame = self.spatial.process(depth_frame)
            depth_frame = self.temporal.process(depth_frame)
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            return color_image, depth_image
        except Exception as e:
            print(f"Error retrieving frames: {e}")
            return None, None

    def get_intrinsics(self):
        return self.intrinsics

    def get_depth_scale(self):
        return self.depth_scale 