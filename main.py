import cv2
import serial
import time
import imutils
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture(0)
ArduinoSerial = serial.Serial('COM3', 9600, timeout=0.1)
time.sleep(1)

detector = FaceMeshDetector(maxFaces=1)
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=1000)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

while cap.isOpened():

    _, frame = cap.read()
    frame = imutils.resize(frame, width=1000)

    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
    difference = cv2.absdiff(frame_bw, start_frame)
    threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
    start_frame = frame_bw

    # cv2.imshow("Cam", threshold)
    if threshold.sum() > 3000000:
        print("found")

    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror the image

    # Face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)  # Detect faces
    for x, y, w, h in faces:
        # Sending coordinates to Arduino
        string = 'X{0:d}Y{1:d}'.format((x + w // 2), (y + h // 2))
        print(string)
        ArduinoSerial.write(string.encode('utf-8'))
        # Plot the region of interest (ROI)
        cv2.rectangle(img, (x-80, y-80), (x + 100 + w, y + 150 + h), (0, 0, 255), 3)
        #cv2.line(img, (0,y+100),(1280,y+100),(0,0,0),2)

    img, faces = detector.findFaceMesh(img, draw=False)
    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]

        # Estimating depth
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.3  # Assuming a constant width for the reference object in the frame
        f = 520  # Focal length of your camera, adjust accordingly
        d = (W * f) / w
        print("Distance:", d)
        cv2.putText(img, "Person Found", (400, 450), cv2.FONT_ITALIC, 1, (0, 0, 255), 2 )

        # Displaying depth on the image
        cvzone.putTextRect(img, f"Distance: {int(d)} cm", (face[10][0] - 120, face[10][1] - (-300)), scale=1.5)

    cv2.imshow('img', img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
