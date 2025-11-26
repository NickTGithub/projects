import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
img = cv.imread('photos/cat.jpg')
cv.imshow('cats', img)

blank = np.zeros(img.shape[:2], dtype='uint8')

# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('gray', gray)

mask = cv.circle(blank, (img.shape[1]//2+100, img.shape[0]//2), 100, 255, -1)

masked=cv.bitwise_and(img,img,mask=mask)
cv.imshow('mask', masked)
#grayscale histogram
# gray_hist = cv.calcHist([gray], [0], mask, [256], [0,256])
#                         ^image(s) ^color channels ^only for a portion? ^histogram size ^range of all possible pixel values
plt.figure()
plt.title('grayscale histo')
plt.xlabel('bins')
plt.ylabel('# of pixels')
colors = ('b', 'g', 'r')
for i,col in enumerate(colors):
    hist = cv.calcHist([img], [i], mask, [256], [0,256])
    plt.plot(hist, color=col)
    plt.xlim([0,255])

# plt.plot(gray_hist)
# plt.xlim([0,256])
plt.show()

cv.waitKey(0)