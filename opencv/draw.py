import cv2 as cv
import numpy as np

#creates blank image with dimensions of 500x500, dtype='unit8' sets the data type to an image, the 3 is number of color channels
blank = np.zeros((500, 500, 3), dtype='uint8')
cv.imshow('Blank', blank)

#1. Paint image certain color
#"[:]" references all the pixels, do smth like [200:300, 300:400] for a certain range (width range, height range)
#---COLOR CODES---
#green=0,255,0
#red=0,0,255
#white=255,255,255
#blue-255,0,0
blank[200:300, 300:400] = 0, 255, 0
cv.imshow('Green', blank)

#2. Draw a rectangle
#cv.rectange(image to do stuff on, point 1, point 2, color, thickness)
#instead of thickness you can put thickness=cv.FILLED, which fills the whole thing, or thickness=-1 does the same thing
cv.rectangle(blank, (0,0), (250,250), (0,255,0), thickness=cv.FILLED)
cv.imshow('Rectange', blank)

#3. Draw a circle
#cv.circle(image, center, radius, color, thickness)
cv.circle(blank, (250,250), 40, (0,0,255), thickness=3)
cv.imshow('Circle', blank)

#4. Draw a line
cv.line(blank, (0,0), (250,250), (255,255,255), thickness=3)
cv.imshow('line', blank)

#5. Text
#cv.putText(image, msg, spot to write, font, scale, color, thickness)
cv.putText(blank, 'Hello_world', (250,250), cv.FONT_HERSHEY_TRIPLEX, 1.0, (255,0,0), thickness=2)
cv.imshow('Hello', blank)
cv.waitKey(0)
