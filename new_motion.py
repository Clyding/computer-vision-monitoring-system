import numpy as np
import cv2
from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import time

# Load the pre-trained YOLO model for face detection
model_weights = '/home/clyderpi/darknet/yolov3.weights'
model_config = '/home/clyderpi/darknet/cfg/yolov3.cfg'
net = cv2.dnn.readNetFromDarknet(model_config, model_weights)

GPIO.setmode(GPIO.BCM)
pir = 7
GPIO.setup(pir, GPIO.IN)
GPIO.setwarnings(False)

# Initialize camera
cap = None
frame_width = None
frame_height = None

# YOLO model settings
confidence_threshold = 0.5
nms_threshold = 0.4

while True:
    foundMotion = GPIO.input(pir)
    if foundMotion == 0:
        if cap is not None:
            cap.release()
            cap = None
            frame_width = None
            frame_height = None
        print("No Motion is detected")
        time.sleep(2)
    elif foundMotion == 1:
        if cap is None:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error while trying to open camera. Please check again.")
                exit()
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("Motion Detected")

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Apply Gaussian blur to the frame
                blurred_frame = cv2.GaussianBlur(frame, (99, 99), 0)

                # Perform face detection using YOLO
                blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
                net.setInput(blob)
                layer_names = net.getLayerNames()
                output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
                detections = net.forward(output_layers)

                # Parse YOLO detection results
                height, width = frame.shape[:2]
                class_ids = []
                confidences = []
                boxes = []
                for output in detections:
                    for detection in output:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > confidence_threshold:
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)
                            class_ids.append(class_id)
                            confidences.append(float(confidence))
                            boxes.append([x, y, w, h])

                # Apply non-maximum suppression
                indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
                for i in indices:
                    i = i[0]
                    x, y, w, h = boxes[i]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Save the video
                out.write(frame)

                # Display the frame
                cv2.imshow('Video', frame)

                # Press 'q' to exit
                if cv2.waitKey(1) == ord('q'):
                    break
            else:
                break

# Release the video capture and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()
