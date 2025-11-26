import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get frame dimensions
    height, width, _ = frame.shape

    # Choose a pixel (e.g., center of the frame)
    pixel_x = width // 2
    pixel_y = height // 2

    # Get BGR values of the pixel
    b, g, r = frame[pixel_y, pixel_x]

    # Convert frame to HSV and get HSV values of the pixel
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = hsv_frame[pixel_y, pixel_x]

    # Display the color information on the frame
    text = f"BGR: ({b},{g},{r}) HSV: ({h},{s},{v})"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Draw a circle at the sampled pixel
    cv2.circle(frame, (pixel_x, pixel_y), 5, (0, 255, 255), -1)

    cv2.imshow('Pixel Color Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('w'):
        print(b,g,r,h,s,v)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()