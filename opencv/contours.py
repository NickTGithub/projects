import cv2 as cv
import numpy as np
#contours = edges

img = cv.imread('Photos/cat.jpg')
cv.imshow('Cats', img)

blank = np.zeros(img.shape, dtype='uint8')
cv.imshow('bnka', blank)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray', gray)

# blur = cv.GaussianBlur(gray, (3,3), cv.BORDER_DEFAULT)
# #      ^many types            ^must be odd
# cv.imshow('Blur', blur)

canny = cv.Canny(gray, 125, 175)
cv.imshow('edge', canny)

ret, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
cv.imshow('thresh', thresh)

contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
#                        ^looks at edges found, returns two values (contours and hierarchies)
print(f'{len(contours)}contours(s) found!')

cv.drawContours(blank, contours, -1, (0,0,255), 2)
cv.imshow('contours drawn', blank)

cv.waitKey(0)