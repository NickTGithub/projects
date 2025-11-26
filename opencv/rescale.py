import cv2 as cv

#---RESIZE IMAGE---

img = cv.imread('Photos/cat.jpg')
cv.imshow('Cat', img)

#have two arguments (frame and scale, set scale to smth)
#works for images, videos, live video
def rescaleFrame(frame, scale=0.5):
    #frame.shape[1] is width of image, frame.shape[0] is height of image
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    #set dimensions to width and height
    dimensions = (width, height)
    #like when you do brain.inertial() it returns smth, this function returns those values below (dimensions of og frame, new frame, and area??)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
    
resized_image = rescaleFrame(img)
cv.imshow('Image', resized_image)    
cv.waitKey(0)

#only works for live video
#in capture.set, the 3 references the width and the 4 references the height
def changeRes(width,height):
    capture.set(3, width)
    capture.set(4, height)

#---RESIZE VIDEO---

capture = cv.VideoCapture('Videos/dog.mp4')

while True:
    isTrue, frame = capture.read()

    frame_resized = rescaleFrame(frame)

    cv.imshow('Video', frame)
    cv.imshow('Video_resized', frame_resized)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()