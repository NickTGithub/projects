import cv2 as cv

img = cv.imread('Photos/cat.jpg')
cv.imshow('Cat', img)

#grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('GRAY', gray)

#blur
blur = cv.GaussianBlur(img, (3,3), cv.BORDER_DEFAULT)
#      ^many types            ^must be odd
cv.imshow('Blur', blur)

#edge cascade (find edges)
canny = cv.Canny(img, 125, 175)
#                      ^bigger=less edges(for both)
cv.imshow('canny', canny)

#dilating image (thicken edges)
dilated = cv.dilate(canny, (11,11), iterations=3)
cv.imshow('dilated', dilated)

#erode (opposite of dilate)
eroded = cv.erode(dilated, (11,11), iterations=3)
cv.imshow('eroded', eroded)

#resize 
resize = cv.resize(img, (500,500), interpolation=cv.INTER_LINEAR)
#        resizes img to this ^ big                  ^when shrinking use cv.INTER_AREA, when scaling up use cv.INTER_LINEAR or cv.INTER_CUBIC <-slower but higher res
cv.imshow('resize', resize)

#cropping
crop = img[50:200, 200:400]
#          ^xrange  ^yrange
cv.imshow('crop', crop)

cv.waitKey(0)