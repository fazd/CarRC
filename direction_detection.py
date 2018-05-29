import numpy as np 
import cv2
from os import listdir
from os.path import isfile, join

class Direction_Detection:

    def __init__(self,img):
        """ Constructor de la clase de direccion
        Parameters
        ----------
        img : imagen que será analizada
        """
        self.img = img


    def __showImage(self,img, name):
        """"Subrutina para mostrar los videos e imagenes
        Parameters
        ----------
        img : imagen que será mostrada 
        """
        cv2.imshow(name,img)


    def __draw_circle(self,img, contour,maximo):

        """
        Funcion que se encarga de dibujar un circulo en el area 
        si es posible encerrar alguna señal de direccion

        Parameters
        ----------
        img : imagen donde se podrá dibujar
        contour : contorno donde se dibujará el circulo
        maximo : area del contorno maximo
        
        Returns
        -------
        img : la imagen con o sin el circulo
        sw : decisión si se pudo o no dibujar el circulo
        side: si sw es verdadero la direccion hacia donde hay que ir 

        """

        if contour is not None:
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
                return img,True, side

        return img,False,"sudo"


    def __masking_image(self,img):

        """
        Esta funcion se encarga de preparar la imagen aislando los colores que nos 
        interesa

        Parameters
        ----------
        img: imagen que queremos aislar

        Returns
        -------

        mask_yellow :retorna mascara con el color deseado resaltado
        """


        height, width,_ = img.shape
        
        im2 = img
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        
        l_yellow = np.array([0, 80, 80], dtype = np.uint8) 
        u_yellow = np.array([220, 255, 255], dtype=np.uint8)
        mask_yellow = cv2.inRange(img_hsv, l_yellow, u_yellow)
        self.__showImage(mask_yellow,"mask definitva")        
        return mask_yellow, mask_yellow


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
        img_tots,contours, hierarchy = cv2.findContours(thresh, 
            cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        maximo = 0
        for contour in contours:
            maximo = max(maximo,cv2.contourArea(contour))
        
        biggest_contour = None
        mask = np.zeros(image.shape, np.uint8)
        if len(contour_sizes) > 0:
            
            biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
            cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
        return biggest_contour,maximo, mask


    def __fix(self,img,x,y):

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

        kernel = np.ones((x,y),np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return opening

    def principal (self):

        """
        Esta función se encarga de controlar todo dentro de la clase

        Returns
        -------

        circle_img: imagen con un posible circulo
        decision: decision si existia o no una señal
        dir: dirección de la señal si existe
        """

        image = cv2.resize(self.img, (480, 360)) 
        img, img_bw = self.__masking_image(image)
        img_bw = self.__fix(img_bw,1,2)
        bc,maximo, mask = self.__find_biggest_contour(img_bw)
        self.__showImage(mask,"mask")
        circle_img,decision,dir = self.__draw_circle(image,bc,maximo)
        return circle_img,decision,dir


