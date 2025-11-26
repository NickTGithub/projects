import cv2
import numpy as np

# Create a blank white image
img = np.ones((400, 400, 3), dtype=np.uint8) * 255

pink_gradient_bgr = [
    (230, 220, 255),
    (215, 200, 255),
    (203, 192, 255),
    (193, 182, 255),
    (180, 105, 255),
    (165, 60, 255),
    (147, 20, 255),
    (133, 21, 199),
    (125, 0, 180),
]

# Draw horizontal stripes
for i, color in enumerate(pink_gradient_bgr):
    y = i * 40
    cv2.rectangle(img, (0, y), (400, y + 40), color, -1)

cv2.imshow("Pink Gradient", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
