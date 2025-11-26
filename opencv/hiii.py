import cv2
import numpy as np

delay = 0

light = np.zeros((500, 500, 3), dtype='uint8')
light[0:500, 0:500] = 255,255,255 #white 128
cv2.imshow('light', light)
cv2.waitKey(delay)
light[0:500, 0:500] = 255,0,0 #blue 238
cv2.imshow('light1', light)    
cv2.waitKey(delay)    
light[0:500, 0:500] = 0,255,0 #green 122
cv2.imshow('light2', light)
cv2.waitKey(delay)
light[0:500, 0:500] = 0, 0, 255 #red 4
cv2.imshow('light3', light)
cv2.waitKey(delay)
light[0:500, 0:500] = 0,255,255 #yellow 62
cv2.imshow('light4', light)  
cv2.waitKey(delay)  
light[0:500, 0:500] = 50, 205, 154 #yellow-green 90
cv2.imshow('light5', light)
cv2.waitKey(delay)
light[0:500, 0:500] = 66, 204, 255 #yellow-orange 36 ----
cv2.imshow('light6', light)
cv2.waitKey(delay)
light[0:500, 0:500] = 127,127,127 #gray 86 --
cv2.imshow('light7', light)
cv2.waitKey(delay)
light[0:500, 0:500] = 0,165,255 #orange 25
cv2.imshow('light8', light)
cv2.waitKey(delay)
light[0:500, 0:500] = 255,255,0 #green-blue 179 ----
cv2.imshow('light9', light)
cv2.waitKey(delay)
light[0:500, 0:500] = 255, 0, 200 #purple 273 --
cv2.imshow('light10', light)
cv2.waitKey(delay)
light[0:500, 0:500] = 255, 0, 255 #violet 304 ----
cv2.imshow('light11', light)
cv2.waitKey(delay)
light[0:500,0:500] = 73, 83, 255 #red-orange
cv2.imshow('light12', light)
cv2.waitKey(0)