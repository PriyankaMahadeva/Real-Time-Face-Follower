import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone

cap = cv2.VideoCapture(0)  # Adjust camera index according to your setup
detector = FaceMeshDetector(maxFaces=1)

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)
    
    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]
        
        # cv2.line(img, pointLeft, pointRight, (0, 200, 0), 3)
        # cv2.circle(img, pointLeft, 5, (255, 0, 255), cv2.FILLED)
        # cv2.circle (img, pointRight, 5, (255, 0, 255), cv2.FILLED)

        # Estimating depth
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.3
        # d=50
        # f = (w*d)/W
        # print(f)
        f= 520
        d = (W * f) / w
        print("Distance: ", d)

        # Displaying depth on the image
        cvzone.putTextRect(img, f"Distance: {int(d)} cm", (face[10][0] - 120, face[10][1] - (-300)), scale=1.5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
