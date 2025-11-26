import cv2

cap = cv2.VideoCapture(0)
x_start = 120 #defines cropping of image
x_end = 525
y_start = 20
y_end = 425

while True:
    #read new frame
    ret, big_frame = cap.read()

    #crop frame
    frame = big_frame[y_start:y_end, x_start:x_end]
    cv2.line(frame, (190, 202), (215, 202), (0,255,0), 2)
    cv2.line(frame, (202, 190), (202, 215), (0,255,0), 2)
    cv2.imshow('Cropped 1', frame)

    key = cv2.waitKey(1) & 0xFF   
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows