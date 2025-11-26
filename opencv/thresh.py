import cv2 as cv

img = cv.imread('photos/cat.jpg')
cv.imshow('cat', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('GRAY', gray)

#simple thresholding
threshold, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
#         if pixel value is above this ^ set to ^   ^ tells it to do that
cv.imshow('simple thresholded', thresh)

# inverse simple
threshold, thresh_inv = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV)
cv.imshow('inv thresh', thresh_inv)

# adaptive thresh

cv.waitKey(0)