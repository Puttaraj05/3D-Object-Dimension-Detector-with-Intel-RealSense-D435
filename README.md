# 3D Object Dimension Detector with Intel RealSense D435

This project is a real-time 3D object dimension detection system using the Intel RealSense D435 camera. It’s ideal for applications like airport baggage scanning, industrial measurement, or logistics automation.

---

## 🚀 Features
- 📸 Captures real-time RGB + depth data using Intel RealSense
- 📦 Detects the largest object in the frame (e.g., bag, box)
- 📏 Calculates Length, Width, and Height in centimeters
- 🎯 Uses depth map and camera intrinsics for true 3D size
- 📉 Displays frame rate (FPS) for performance monitoring

---

## 📁 Project Structure

```
project_folder/
├── main.py                   # Main execution script
├── realsense_camera.py      # Camera setup and frame capture
├── object_detector.py       # Detects largest object using contours
├── dimension_estimator.py   # Converts depth to 3D size
├── visualizer.py            # Overlays measurements and FPS
├── requirements.txt         # Python dependencies
```

---

## ⚙️ Requirements
- Python 3.8+
- Intel RealSense D435

### 📦 Python Dependencies

Install them all with:

```bash
pip install -r requirements.txt
```

> **Note:** You must install Intel’s `pyrealsense2`. If installation fails, refer to the [RealSense SDK for macOS](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_osx.md).

---

## ▶️ How to Run
1. Connect the RealSense D435 to a USB 3.0 port
2. Activate your virtual environment (optional but recommended)
3. Run the main program:

```bash
python main.py
```

Press `q` to exit the visualization window.

---

## 🧪 Output Example
- A bounding box around detected object
- Printed text: `L: 55.2cm  W: 33.1cm  H: 21.8cm`
- FPS counter for performance

---

## 📌 Notes
- Ensure good lighting and background contrast
- Keep the camera fixed and object placed on a flat surface
- Accuracy improves with clean contours and valid depth data

---

## 📄 License

This project is provided for academic and prototyping use. For commercial use, please contact the author.

---

## 🙋 Need Help?

If you need assistance or want to expand this to object classification, scene scanning, or point cloud analysis, just ask! 