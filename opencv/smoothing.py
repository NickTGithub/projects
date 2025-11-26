import cv2 as cv

img = cv.imread('Photos/cat.jpg')
cv.imshow('Cat', img)

# averaging
avg = cv.blur(img, (3,3))
#                   ^ increase this, increase blur
cv.imshow('average', avg)

# gaussian
gaus = cv.GaussianBlur(img, (3,3), 0)
#      ^many types            ^must be odd
cv.imshow('gaussian', gaus)

# median
med = cv.medianBlur(img, 3)
cv.imshow('med', med)

# bilateral (keeps edges)
bilat = cv.bilateralFilter(img, 5, 15, 15)
cv.imshow('bilat', bilat)

cv.waitKey(0)