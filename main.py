import cv2
import numpy as np
import time
from Stop_detection import Stop_Detection
from borders import Border
from direction_detection import Direction_Detection




img =cv2.imread("Stop_data_big/131.jpeg")
copia = img
print("flag")
b = Border(img)
borders_img = b.principal("hi")
cv2.imshow("s",borders_img)
cv2.waitKey(0)

s = Stop_Detection(img)
stop_img = s.principal()
cv2.imshow("s",stop_img)
cv2.waitKey(0)

d = Direction_Detection(img)
direction_img = d.principal()
cv2.imshow("s",direction_img)
cv2.waitKey(0)
