import cv2 as cv
import time
import numpy as np
blank = np.zeros((500, 500, 3), dtype='uint8')
cv.imshow('Green', blank)
cv.waitKey(1000)
blank[0:500, 0:500] = 0, 255, 0
cv.imshow('Green', blank)
cv.waitKey(1000)
blank[0:500, 0:500] = 0, 255, 255
cv.imshow('Green', blank)
cv.waitKey(1000)
cv.waitKey(0)
