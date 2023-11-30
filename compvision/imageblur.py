import cv2
import numpy as np
cap = cv2.VideoCapture(0)

cascade_path = cv2.data.haarscascades + "haarscascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

person_id = 1
labels = {}


if (cap.isOpened() == False):
    print('Error while trying to open camera. Plese check again...')
# get the frame width and height
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# define codec and create VideoWriter object
out = cv2.VideoWriter('/, compvision, image_and_video, cam_blur.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
# read until end of video
while(cap.isOpened()):
    # capture each frame of the video
    ret, frame = cap.read()
    if ret == True:
        # add gaussian blurring to frame
        frame = cv2.GaussianBlur(frame, (11, 11), 0)
        # save video frame
        out.write(frame)
        # display frame
        cv2.imshow('Video', frame)
        # press `q` to exit
        if cv2.waitKey(27) & 0xFF == ord('q'):
            break

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLORBGR2GRAY)

    faces = face_cascade.detectMultiSCale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        if person_id not in labels:
            labels[person_id] = "person {}".format(person_id)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, labels[person_id], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        person_id += 1

    cv2.imshow("Person Detection", frame)


# release VideoCapture()
cap.release()
# close all frames and video windows
cv2.destroyAllWindows()