import cv2
import numpy as np
from PIL import Image
import time
import threading

color = [255, 255, 255] 
color2 = [180, 65, 255]
color3 = [60,45,115]
font = cv2.FONT_HERSHEY_COMPLEX

stop_threads = False  # <-- Shared flag for all threads

def reset():
    global row, column, row_space, column_space, og_x1, og_y1, squares, width, height
    if 'width' not in globals() or 'height' not in globals():
        width = 0
        height = 0
    row = 0
    column = 0
    row_space = width / 8
    column_space = height / 8
    og_x1 = x1
    og_y1 = y1
    squares = np.zeros((8,8), dtype=int)

def get_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c,cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 0, 0, 100
    upperLimit = hsvC[0][0][0] + 0, 100, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit

def get_limits2(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c,cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 0, 48, 80
    upperLimit = hsvC[0][0][0] + 20, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit

cap = cv2.VideoCapture(0)

high_x = 0
low_x = 500
high_y = 0
low_y = 500
y_start = 20
y_end = 425
x_start = 120
x_end = 525
x1=0
y1=0
x2=0
y2=0
lock = 0
lock2 = 0
s5=np.zeros((8,8), dtype=int)
s4=np.zeros((8,8), dtype=int)
s3=np.zeros((8,8), dtype=int)
s2=np.zeros((8,8), dtype=int)
s1=np.zeros((8,8), dtype=int)
new = np.zeros((8,8), dtype=int)
old = np.zeros((8,8), dtype=int)
hand = 3
squares = np.zeros((8,8), dtype=int)
key = cv2.waitKey(1) & 0xFF  
bbox_ = (0,0,1,1)

def comp():
    global s1, s2, s3, s4, s5, squares, hand, new, old, key, stop_threads
    row=0
    column=0
    while not stop_threads:
        if hand == 0:
            row = 0
            column = 0
            for q in range (8):
                for w in range (8):
                    if (s1[column, row] + s2[column, row] + s3[column, row] + s4[column, row] + s5[column, row]) >= 4:
                        new[column,row] = 1
                    else:
                        new[column,row] = 0
                    column = column + 1
                row = row + 1
            row = 0
            column = 0
            for r in range (8):
                for t in range (8):
                    if (old[column, row] - new[column, row]) == 1:
                        print('piece gone', column, row)
                    else:
                        print('new piece', column, row)
                    column = column + 1
                row = row + 1
        if key == ord('q'):
            stop_threads = True
            break

def hand_check():
    global hand, bbox_, key, stop_threads
    while not stop_threads:
        if bbox_ is not None:
            hand = 1
        else: 
            hand = 0
        if key == ord('q'):
            stop_threads = True
            break

def main_():
    global bbox_, bbox, squares, s1, s2, s3, s4, s5, width, height, x1, x2, y1, y2, x1_, x2_, y1_, y2_, row, column, row_space, column_space, og_x1, og_y1, key, lock, stop_threads
    while not stop_threads:

        s5 = s4
        s4 = s3
        s3 = s2
        s2 = s1
        s1 = squares

        ret, big_frame = cap.read()

        cv2.imshow('OG 1', big_frame)

        frame = big_frame[y_start:y_end, x_start:x_end]

        blank = np.zeros(frame.shape[:2], dtype='uint8')

        cv2.imshow('Cropped 2', frame)
        resize = cv2.resize(frame, (500,500), interpolation=cv2.INTER_LINEAR)

        hsvimg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        lowerLimit, upperLimit = get_limits2(color=color3)

        mask = cv2.inRange(hsvimg, lowerLimit, upperLimit)

        mask_ = Image.fromarray(mask)

        bbox_ = mask_.getbbox()

        if bbox_ is not None:
            x1_, y1_, x2_, y2_ = bbox_

        grayimg = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        if lock == 0:
            hsvimg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

            lowerLimit, upperLimit = get_limits(color=color)

            mask = cv2.inRange(hsvimg, lowerLimit, upperLimit)

            mask_ = Image.fromarray(mask)

            bbox = mask_.getbbox()

            if bbox is not None:
                x1, y1, x2, y2 = bbox
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)

                frame = cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 5)

            cv2.imshow('Color Detect 4', frame)

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        rectangle = cv2.rectangle(blank, (x1,y1), (x2,y2), 255, -1)

        masked = cv2.bitwise_and(frame,frame,mask=rectangle)
        cv2.imshow('Masked 5', masked)

        grayimg = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

        canny = cv2.Canny(grayimg, 150, 150, 3, L2gradient=True)

        ret, thresh = cv2.threshold(grayimg, 125, 255, cv2.THRESH_BINARY)

        contours, hierarchies = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(masked, contours, -1, (0,0,255), 1)

        cv2.imshow('Contours+Color 6', masked)

        width = int(x2-x1)
        height = int(y2-y1)

        reset()

        key = cv2.waitKey(1) & 0xFF        
        if key == ord('q'):
            stop_threads = True
            break

    cap.release()
    cv2.destroyAllWindows()

compare = threading.Thread(target=comp)
check_hand = threading.Thread(target=hand_check)
main = threading.Thread(target=main_)

compare.start()
check_hand.start()
main.start()
