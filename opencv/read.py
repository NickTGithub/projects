import cv2 as cv

#---READING IMAGES---

#read image as matrix of pixels
img = cv.imread('Photos/cat.jpg')

#displays matrix in new window
cv.imshow('Cat', img)

#waits indefinetly 
cv.waitKey(0)

#---READING VIDEOS---

#either use "'smth.mp4'" or put an integer inside the () to select camera (0=webcam, 1=first external camera, etc.)
capture = cv.VideoCapture(0)

#reads video frame by frame
while True:
    isTrue, frame = capture.read()
    cv.imshow('Video', frame)
    #if letter d is pressed on keyboard, break out of loop and stop video
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

#stop capturing frames and destroy all windows
capture.release()
cv.destroyAllWindows()
#IMPORTANT: if "error: (-215:Assertion failed)" shows up in the terminal it means there isn't any file to pull
#          --->the video/image isn't in the specified path location or the video is out of frame