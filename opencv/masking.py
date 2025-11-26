import cv2 as cv
import numpy as np

img = cv.imread('photos/cat.jpg')
cv.imshow('cat', img)

blank = np.zeros(img.shape[:2], dtype='uint8')
cv.imshow('blank', blank)

circle = cv.circle(blank.copy(), (img.shape[1]//2+100, img.shape[0]//2), 100, 255, -1)
#                   ^copies blank  ^x-coord of center   ^ycoord        ^radius ^color  ^fill

rectangle = cv.rectangle(blank.copy(), (100,30), (470,370), 255, -1)
#                        ^copies blank   ^corner   ^other corner ^color ^fill

cv.imshow('rectangle', rectangle)
cv.imshow('circle', circle)
weird = cv.bitwise_and(rectangle,circle)
cv.imshow('weird', weird)

masked = cv.bitwise_and(img,img,mask=weird)
cv.imshow('masked', masked)

cv.waitKey(0)