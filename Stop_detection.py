import numpy as np 
import cv2
from os import listdir
from os.path import isfile, join
from picamera import PiCamera
from picamera.array import PiRGBArray
from edges import Driver
import time

class Stop_Detection:

    def __init__(self, img):
        """ Constructor de la clase de Stop_Detection
        Parameters
        ----------
        img : imagen que será analizada
        """

        self.img = img

    def __draw_circle(self,img, contour,maximo):

        """
        Funcion que se encarga de dibujar un circulo en el area 
        si es posible encerrar alguna señal de stop

        Parameters
        ----------
        img : imagen donde se podrá dibujar
        contour : contorno donde se dibujará el circulo
        maximo : area del contorno maximo
        
        Returns
        -------
        img : la imagen con o sin el circulo
        sw : decisión si se pudo o no dibujar el circulo

        """
        if contour is not None:
            (x,y),radius = cv2.minEnclosingCircle(contour)
            center = (int(x),int(y))
            radius = int(radius)
            area = 3.14*radius**2
            if area >= maximo:
                if 0.45*area < maximo:
                    if area >= 4000:
                        sw = True
                    else:
                        sw = False
                else:
                    sw = False
            else:
                if 0.45*maximo < area:
                    if area >= 3000:
                        sw = True
                    else:
                        sw = False
                else:
                    sw = False

            if(sw):
                cv2.circle(img,center,radius,(0,255,0),2)
                return img,sw
            
        return img,False

    def __showImage(self,img, name):

        """"Subrutina para mostrar los videos e imagenes
        Parameters
        ----------
        img : imagen que será mostrada 
        """
        cv2.imshow(name,img)

    
    def __fix(self,img):

        """Esta función se encarga de mejorar la imagen con operacion
        de opening 

        Parameters
        ----------
        img: imagen que queremos mejorar
        x: valor para la función de opening
        y: valor para la función de opening 

        Returns
        -------

        opening: imagen mejorada

        """

        kernel = np.ones((1,2),np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return opening

    def __preliminar_image(self,img,name):

        """
        Esta funcion se encarga de preparar la imagen aislando los colores que nos 
        interesa

        Parameters
        ----------
        img: imagen que queremos aislar
        name: nombre de la imagen

        Returns
        -------

        filter_img :retorna mascara con el color deseado resaltado
        filter_byw : mascara a blanco y negro
        """


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


        """
        Esta función se encarga de encontrar el contorno mas grande de la mascara

        Parameters
        ----------
        image: esta es la mascara 

        Returns
        -------

        biggest_contour : el contorno mas grande encontrado
        maximo : el tamaño del contorno mas grande encontrado
        mask: la mascara usada para dibujar el contorno


        """
        
        ret, thresh = cv2.threshold(image, 50,255, 0)
        img_tots,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Isolate largest contour

        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        #print("inicio:")
        maximo = 0
        for contour in contours:
            maximo = max(maximo,cv2.contourArea(contour))
        biggest_contour = None
        #print("area cont:",maximo)
        mask = np.zeros(image.shape, np.uint8)
        if len(contour_sizes)  > 0:        
            biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
            cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
        #showImage(mask,"mask")
        return biggest_contour,maximo, mask


    def principal(self):
        """
        Esta función se encarga de controlar todo dentro de la clase

        Returns
        -------

        circle_img: imagen con un posible circulo
        decision: decision si existia o no una señal
        """

        image = cv2.resize(self.img, (480, 360)) 
        #preliminar_image(image,"prel")
        img, img_bw = self.__preliminar_image(image,"prel")
        img_bw = self.__fix(img_bw)
        #self.__showImage(img_bw,"mask")
        #showImage(img_bw,"img_byw")
        bc,maximo, mask = self.__find_biggest_contour(img_bw)
        circle_img, decision =self.__draw_circle(image,bc,maximo)
        return circle_img, decision
