import numpy as np 
import cv2
from os import listdir
from os.path import isfile, join

class Stop_Detection:

    def __init__(self, img):
        self.img = img

    def __draw_circle(self,img, contour,maximo):
        (x,y),radius = cv2.minEnclosingCircle(contour)
        center = (int(x),int(y))
        radius = int(radius)
        area = 3.14*radius**2
        if area >= maximo:
            if 0.45*area < maximo:
                sw = True
            else:
                sw = False
        else:
            if 0.45*maximo < area:
                sw = True
            else:
                sw = False

        if(sw):
            cv2.circle(img,center,radius,(0,255,0),2)
        
        #print("area C:",radius*radius*3.14)
        #print("area con:",contour)
        #self.__showImage(img,"circle")
        return img

    def __showImage(self,img, name):
        cv2.imshow(name,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __fix(self,img):
        kernel = np.ones((1,2),np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return opening

    def __preliminar_image(self,img,name):
        height, width, _ = img.shape
        #self.__showImage(img,name)
        img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        kernel_size = (3,3)
        gauss_img = cv2.GaussianBlur(img,kernel_size,0)
        
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        
        l_red_hsv = np.array([0, 100, 100], dtype = np.uint8)
        u_red_hsv = np.array([10, 255, 255], dtype = np.uint8)
        l_red_hsv2 = np.array([160, 100, 100], dtype = np.uint8)
        
        u_red_hsv2 = np.array([179, 255, 255], dtype = np.uint8)
        red_mask_hsv1 = cv2.inRange(img_hsv,l_red_hsv,u_red_hsv)
        red_mask_hsv2 = cv2.inRange(img_hsv,l_red_hsv2,u_red_hsv2)
        red_mask_hsv = red_mask_hsv1 + red_mask_hsv2
        
        l_red = np.array([0,0, 80], dtype = np.uint8)
        u_red = np.array([50,50, 255], dtype = np.uint8)
        red_mask = cv2.inRange(img, l_red, u_red)
        
        filter_byw = red_mask +red_mask_hsv 
        filter_img = cv2.bitwise_and(gauss_img, gauss_img, mask=cv2.bitwise_or(red_mask,red_mask_hsv))
        
        return filter_img, filter_byw
        
    def __find_biggest_contour(self,image):
        
        ret, thresh = cv2.threshold(image, 50,255, 0)
        img_tots,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Isolate largest contour

        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        #print("inicio:")
        maximo = 0
        for contour in contours:
            maximo = max(maximo,cv2.contourArea(contour))

        #print("area cont:",maximo)

        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

        mask = np.zeros(image.shape, np.uint8)
        cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
        #showImage(mask,"mask")
        return biggest_contour,maximo, mask


    def principal(self):
        image = cv2.resize(self.img, (480, 360)) 
        #preliminar_image(image,"prel")
        img, img_bw = self.__preliminar_image(image,"prel")
        img_bw = self.__fix(img_bw)
        #showImage(img_bw,"img_byw")
        bc,maximo, mask = self.__find_biggest_contour(img_bw)
        circle_img =self.__draw_circle(image,bc,maximo)
        return circle_img



"""
mypath = "Stop_data_big/"
onlyimg = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for img in onlyimg:
    #print("in image") 
    img = mypath+img
    image = cv2.imread(img)
    i = Stop_Detection(image)
    i.principal()
    image = cv2.resize(image, (480, 360)) 
    #preliminar_image(image,"prel")
    img, img_bw = preliminar_image(image,"prel")
    img_bw = fix(img_bw)
    #showImage(img_bw,"img_byw")
    bc,maximo, mask = find_biggest_contour(img_bw)
    draw_circle(image,bc,maximo)"""
