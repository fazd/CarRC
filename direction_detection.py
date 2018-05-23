import numpy as np 
import cv2
from os import listdir
from os.path import isfile, join

class Direction_Detection:

    def __init__(self,img):
        self.img = img


    def __showImage(self,img, name):
        cv2.imshow(name,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def __draw_circle(self,img, contour,maximo):
        height, width,_ = img.shape
        (x,y),radius = cv2.minEnclosingCircle(contour)
        #print("center : ",x,y)
        center = (int(x),int(y))
        radius = int(radius)
        area = 3.14*radius**2
        if x < height/2:
            side = "Left"
        else:
            side = "Right"

        if area >= maximo:
            if 0.3*area < maximo:
                sw = True
            else:
                sw = False
        else:
            if 0.3*maximo < area:
                sw = True
            else:
                sw = False

        if(sw):
            cv2.circle(img,center,radius,(0,255,0),2)
            cv2.putText(img,side, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 200)
        
        #print("area C:",radius*radius*3.14)
        #print("area con:",contour)
        #self.__showImage(img,"circle")
        return img


    def __masking_image(self,img):
        height, width,_ = img.shape
        #self.__showImage(img,"normal")
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        #showImage(img_hsv,"hsv")

        l_yellow = np.array([0, 160, 220], dtype = np.uint8) 
        u_yellow = np.array([25, 255, 255], dtype=np.uint8)
        yellow_mask = cv2.inRange(img,l_yellow,u_yellow)
        
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        black_mask = cv2.inRange(img_gray,0,20)
        #showImage(img_gray,"gray")
        black_mask = self.__fix(black_mask, 3,3)
        #showImage(black_mask,"black")
        #showImage(yellow_mask,"yellow_mask")
        filter_bw = yellow_mask + black_mask
        filter_img = cv2.bitwise_or(img, img, 
            mask=cv2.bitwise_or(yellow_mask,black_mask))
        #self.__showImage(filter_img,"filter img")
        #showImage(black_mask,"black mask")
        return filter_img,filter_bw


    def __find_biggest_contour(self,image):
        self.__showImage(image,"biggest")
        ret, thresh = cv2.threshold(image, 50,255, 0)
        img_tots,contours, hierarchy = cv2.findContours(thresh, 
            cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        #print("inicio:")
        maximo = 0
        for contour in contours:
            maximo = max(maximo,cv2.contourArea(contour))

        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

        mask = np.zeros(image.shape, np.uint8)
        cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
        #showImage(mask,"mask")
        return biggest_contour,maximo, mask


    def __fix(self,img,x,y):
        kernel = np.ones((x,y),np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return opening

    def principal (self):
        image = cv2.resize(self.img, (480, 360)) 
        #preliminar_image(image,"prel")
        img, img_bw = self.__masking_image(image)
        img_bw = self.__fix(img_bw,1,2)
        #showImage(img_bw,"img_byw")
        bc,maximo, mask = self.__find_biggest_contour(img_bw)
        circle_img = self.__draw_circle(image,bc,maximo)
        return circle_img

"""
mypath = "turn_right/exterior/"
onlyimg = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for img in onlyimg:
    #print("in image") 
    img = mypath+img
    image = cv2.imread(img)
    i = Direction_Detection(image)
    circle_img = i.principal()
    cv2.imshow("img",circle_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

"""