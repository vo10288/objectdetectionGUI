#!/opt/virtualenv/computer_vision/bin/python3

# 20250623
# https://tsurugi-linux.org
# by Visi@n

# Example: object_detection_video_write_video.py -v inputvideo.avi -o outputvideo.mp4

from imutils.video import FPS
from datetime import datetime
import numpy as np
import argparse
import imutils
import time
import cv2
import os

# Argomenti da terminale
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", default="/opt/computer_vision/MobileNetSSD_deploy.prototxt.txt", help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-o", "--output", required=True, help="path to output video file")
ap.add_argument("-m", "--model", default="/opt/computer_vision/MobileNetSSD_deploy.caffemodel", help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
ap.add_argument("-v", "--video", help="name of input video file")
ap.add_argument("-r", "--resolution", type=int, default=800, help="resolution of output video")
args = vars(ap.parse_args())

# Classi COCO
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
           "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
           "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

print("[INFO] starting video stream...")
vs = cv2.VideoCapture(args["video"])
time.sleep(2.0)
fps = FPS().start()
writer = None

try:
    total = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    print("[INFO] {} total video frames".format(total))
except:
    print("[INFO] could not determine # video frames")
    total = -1

# Timer per la stima del tempo del primo frame
frame_timer_start = time.time()

# Percorso output
output_dir = os.path.expanduser('~/02.computer_vision/03.reports/')
os.makedirs(output_dir, exist_ok=True)
os.chdir(output_dir)

frame_number = 0
while True:
    ret, frame = vs.read()
    frame_number += 1
    if not ret:
        break

    frame = imutils.resize(frame, width=args["resolution"])
    (h, w) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > args["confidence"]:
            idx = int(detections[0, 0, i, 1])
            label_name = CLASSES[idx]

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = f"{label_name}: {confidence * 100:.2f}%"
            cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            # Salva frame se oggetto rilevante
            if label_name in ["car", "person", "bicycle", "bus", "motorbike", "bird", "cat", "cow", "dog", "horse", "sheep", "train"]:
                class_folder = label_name.upper() + "S"
                os.makedirs(class_folder, exist_ok=True)
                os.makedirs("ALL", exist_ok=True)
                timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                filename = f"{timestamp}_{label_name}.jpg"
                cv2.imwrite(f"./{class_folder}/{filename}", frame)
                cv2.imwrite(f"./ALL/{filename}", frame)

    # Inizializza writer al primo frame
    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(args["output"], fourcc, 30, (frame.shape[1], frame.shape[0]), True)

        if total > 0:
            elapsed_first_frame = time.time() - frame_timer_start
            print(f"[INFO] single frame took {elapsed_first_frame:.4f} seconds")
            print(f"[INFO] estimated total time to finish: {elapsed_first_frame * total:.2f} seconds")

    writer.write(frame)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    fps.update()

fps.stop()
print(f"[INFO] elapsed time: {fps.elapsed():.2f}")
print(f"[INFO] approx. FPS: {fps.fps():.2f}")

vs.release()
writer.release()
cv2.destroyAllWindows()
