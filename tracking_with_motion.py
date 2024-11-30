import cv2
import serial
import time
import imutils
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Initialize the camera and serial connection
cap = cv2.VideoCapture(0)
ArduinoSerial = serial.Serial('COM3', 9600, timeout=0.1)
time.sleep(1)

# Initialize the FaceMeshDetector
detector = FaceMeshDetector(maxFaces=1)

# Capture the initial frame for background subtraction
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=1000)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

while cap.isOpened():
    # Read the frame
    _, frame = cap.read()
    frame = imutils.resize(frame, width=1000)

    # Perform background subtraction
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
    difference = cv2.absdiff(frame_bw, start_frame)
    threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
    start_frame = frame_bw

    # Flip the thresholded frame horizontally
    threshold = cv2.flip(threshold, 1)
    cv2.imshow("Cam", threshold)

    # If the thresholded frame contains a significant amount of movement
    if threshold.sum() > 30000:
        print("Movement detected")

        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 6)

        # Send face coordinates to Arduino and draw rectangles around faces
        for x, y, w, h in faces:
            string = 'X={0:d}Y={1:d}'.format((x + w // 2), (y + h // 2))
            print(string)
            ArduinoSerial.write(string.encode('utf-8'))
            cv2.rectangle(frame, (x-80, y-80), (x + 100 + w, y + 150 + h), (0, 0, 255), 3)

        # Detect face landmarks and estimate depth
        frame = cv2.flip(frame, 1)
        frame, faces = detector.findFaceMesh(frame, draw=False)
        if faces:
            face = faces[0]
            pointLeft = face[145]
            pointRight = face[374]

            # Estimating depth
            w, _ = detector.findDistance(pointLeft, pointRight)
            W = 6.3  # Assuming a constant width for the reference object in the frame
            f = 950  # Focal length of your camera, adjust accordingly
            d = (W * f) / w
            print("Distance:", d)
            cv2.putText(frame, "Person Found", (700, 700), cv2.FONT_ITALIC, 1, (0, 0, 255), 3 )

            # Display depth on the image
            cvzone.putTextRect(frame, f"Distance: {int(d)} cm", (face[10][0] - (100), face[10][1] - (-450)), scale=1.5)

        # Display the frame
        cv2.imshow('img', frame)

    # Press 'q' to quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
