import numpy as np 
import cv2
from os import listdir
from os.path import isfile, join


def showImage(img, name):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def mask_image(img):

	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)


	l_red = np.array([0, 160, 220], dtype = np.uint8)
	u_red = np.array([0, 160, 220], dtype = np.uint8)


	l_green = np.array([0, 160, 220], dtype = np.uint8)
	u_green = np.array([0, 160, 220], dtype = np.uint8)




cv2.imread("")
