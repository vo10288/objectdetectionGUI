# objectdetectionGUI
Computer Vision object detection
# Object Detection & License Plate Recognition GUI

This project is a Python-based graphical user interface for object detection and license plate recognition using pre-trained MobileNetSSD and OpenALPR.

Created by **Antonio 'Visi@n' Broi** – [tsurugi-linux.org](https://tsurugi-linux.org)

---

## 🧠 Features

- Object detection from:
  - Live webcam stream
  - Video files
  - Output annotated videos
- License plate recognition via OpenALPR
- Automatic saving of detected frames by class (e.g., CARS, PERSONS)
- Interactive GUI using `tkinter`
- Frame-by-frame processing with FPS estimation
- Organized output reports in `~/02.computer_vision/03.reports/`

---

## 🖼️ GUI File: `objectdetectionGUI.py`

This file launches the graphical interface where the user can:

- Start/stop webcam or video detection
- Select input/output files
- Adjust resolution
- Trigger license plate recognition using either OpenALPR CLI or Python bindings
- All outputs are saved in class-based folders and in an `ALL` folder

---

## 🎥 Video Analysis File: `object_detection_video_write_video.py`

This script processes video files frame-by-frame, applies object detection using MobileNetSSD, draws bounding boxes, and saves the result in:

- Output video file (annotated)
- One image per detection for selected classes (e.g., car, person, etc.)
- Organized in timestamped subfolders

Run from CLI:

```bash
python3 object_detection_video_write_video.py -v inputvideo.avi -o outputvideo.avi
