import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Load the pre-trained Haar cascade for face detection
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

# Open video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error while trying to open camera. Please check again.")
    exit()

#GPIO SETUP
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

# Get the frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create a VideoWriter object to save the output
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height))


while True:
        def callback(channel):
                if GPIO.input(channel):
                        print( "Sound Detected!")
                        while cap.isOpened():
    # Capture each frame of the video
                            ret, frame = cap.read()
                        if ret:
                            # Apply Gaussian blur to the frame
                            blurred_frame = cv2.GaussianBlur(frame, (99, 99), 0)

                            # Perform face detection
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                            # Create a mask for background blur
                            mask = np.zeros_like(frame)
                            for (x, y, w, h) in faces:
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                mask[y:y+h, x:x+w] = blurred_frame[y:y+h, x:x+w]

                            # Apply the mask to blur the background
                            blurred_frame = cv2.GaussianBlur(frame, (99, 99), 0)
                            frame = np.where(mask == 0, blurred_frame, frame)

                            # Save the video
                            out.write(frame)

                            # Display the frame
                            cv2.imshow('Video', frame)

                            # Press 'q' to exit
                            if cv2.waitKey(1) == ord('q'):
                                break
                            else:
                                break

                # else:
                #         print("Sound Detected!")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

# Release the video capture and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()
