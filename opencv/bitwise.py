import cv2 as cv
import numpy as np

blank = np.zeros((400,400),dtype='uint8')

rectangle = cv.rectangle(blank.copy(), (30,30), (370,370), 255, -1)
circle = cv.circle(blank.copy(), (200,200), 200, 255, -1)

cv.imshow('rect', rectangle)
cv.imshow('ciurc', circle)

# bitwise AND (returns intersecting sections)
bitwise_and = cv.bitwise_and(rectangle, circle)
cv.imshow('and', bitwise_and)

# OR (combines images)
bitwise_or = cv.bitwise_or(rectangle,circle)
cv.imshow('or', bitwise_or)

# XOR (non-intersecting regions)
bitwise_xor = cv.bitwise_xor(rectangle, circle)
cv.imshow('xor', bitwise_xor)

# NOT (inverts color of image)
bitwise_not = cv.bitwise_not(rectangle)
cv.imshow('not', bitwise_not)
cv.waitKey(0)