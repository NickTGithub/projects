import cv2
import numpy as np
from PIL import Image

color = [255,255,255] #BGR

#[0,255,0] is green
#[255,0,0] is blue
#[0,0,255] is red
#[0,255,255] is yellow
#[255,0,255] is magenta


def get_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c,cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 0, 100, 100
    upperLimit = hsvC[0][0][0] + 0, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)
    print(lowerLimit, upperLimit)

    return lowerLimit, upperLimit

cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()

    hsvimg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=color)

    mask = cv2.inRange(hsvimg, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 5)

    #print(bbox)

    cv2.imshow('frame', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows
