import numpy as np
import cv2

class Border:

    def __init__(self,img):
        self.img = img
        self.INF = 1000000000
        self.LEFT_B = [(0,0,0,0)]
        self.RIGHT_B = [(0,0,0,0)]

    def __showImg(self,img):
        cv2.imshow('image',img)
        cv2.waitKey(0)

    def __ImportantArea(self,img, vertices):
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, [vertices], 255)
        n = len(vertices)
        img = cv2.bitwise_and(img,mask)
        return img

    def __slope(self,line):
        #print(line)
        x1,y1,x2,y2 = line[0]
        if(x2-x1) == 0:
            return self.INF
        return (y2-y1)/(x2-x1)

    def __eucl(self,line):
        x0,y0,x1,y1 = line[0]
        return np.sqrt((x0-x1)*(x0-x1) + (y0-y1)*(y0-y1))

    def __initial_p(self,line, img, yf):
        y,x,_ = img.shape
        #print(y,x)
        x0,y0,x1,y1 = line[0]
        s = self.__slope(line)
        b = y1- s*x1
        
        #print("la ecuacion sera y=",s,"x+",b)
        #print("x,y es", x0,y0)
        #print("x,y es", x1,y1)
        xi = float((y-b)/s)
        xi = int(xi)
        xf = float((yf-b)/s)
        xf = int(xf)
        return xi,y,xf,yf 


    def __draw_line(self,img, lines, color, dir, y_max, pix = 10):
        global LEFT_B 
        global RIGHT_B
        max_euc = 0
        line_max = [(0,0,0,0)]
        for line in lines:
            for x0,y0,x1,y1 in line:
                if(self.__eucl(line) > max_euc):
                    max_euc = self.__eucl(line)
                    line_max = line
                #cv2.line(img, (x0, y0), (x1, y1), color, pix)

        a,b,c,d = line_max[0]
        if(a == b == c == d == 0):
            #print("entro")
            if(dir == 0):
                line_max = self.LEFT_B
            else:
                line_max = self.RIGHT_B
            #print(line_max)
        else:
            if(dir == 0):
                self.LEFT_B = line_max
            else:
                self.RIGHT_B = line_max
        x0,y0,x1,y1 = self.__initial_p(line_max,img,y_max)
        points = [(x0,y0),(x1,y1)]
        cv2.line(img, (x0, y0), (x1, y1), color, pix)
        return img,points

    def __draw_polygon(self,img, vertices, color):
        vertices = np.array([vertices],dtype = np.int32)
        #print(vertices)
        cv2.fillPoly(img, [vertices], color)
        return img


    def __select_lines(self,img,lines,vertices):
        left = []
        right = []
        v0,v1,_,_ = vertices
        x0,y0 = v0
        x1,y1 = v1
        center = (x0+x1)/2
        for line in lines:
            for x1,y1,x2,y2 in line:
                if(x1 < center):
                    left.append(line)
                else:
                    right.append(line)

        img,points = self.__draw_line(img,left,[255,0,0],0,y0)
        img,points2 = self.__draw_line(img,right,[0,255,0],1,y0)
        points2 = list(reversed(points2))
        points.extend(points2)
        #showImg(img)
        img = self.__draw_polygon(img,points,[0,0,255])
        return img


    def __hough_line (self,img, vertices):
        rho = 1
        theta = np.pi/180
        threshold = 20
        min_line_len = 50
        max_line_gap = 200
        lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
            minLineLength=min_line_len, maxLineGap=max_line_gap)
        height,width = img.shape
        mask = np.zeros((height,width,3),dtype = np.uint8)
        mask = self.__select_lines(mask,lines, vertices)
        #showImg(mask)
        return mask


    def __union (self,img, mask):
        return cv2.addWeighted(img, 0.5, mask, 1, 0)

    def __transform_frame(self,img):
        
        height,width,_ = img.shape
        v0 = (int(600*width/1000),int(670*height/1000))
        v1 = [int(400*width/1000) , int(670*height/1000)]
        v2 = [int(50*width/1000), height]
        v3 = [int(950*width/1000), height] 

        l_yellow = np.array([60, 80, 80], dtype = np.uint8) 
        u_yellow = np.array([105, 255, 255], dtype=np.uint8)
        l_white = np.array([0, 0, 200],dtype = np.uint8)
        u_white = np.array([255,80, 255],dtype = np.uint8)

        vertices = np.array([v0,v1,v2,v3], dtype=np.int32)
        #print(vertices)
        #img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        #showImg(img_hsv)
        kernel_size = (3,3)
        gauss_img = cv2.GaussianBlur(img_hsv,kernel_size,0)
        mask_white = cv2.inRange(img_gray,220,255)
        #mask_white = cv2.inRange(gauss_img,l_white,u_white)
        #showImg(mask_white)
        mask_yellow = cv2.inRange(gauss_img, l_yellow, u_yellow)
        #showImg(mask_yellow)
        filter_img = cv2.bitwise_and(gauss_img, gauss_img, mask=cv2.bitwise_or(mask_white, mask_yellow))
        #showImg(filter_img)
        low_threshold = 100
        high_threshold = 200
        canny_edges = cv2.Canny(filter_img,low_threshold,high_threshold)
        canny_edges = self.__ImportantArea(canny_edges,vertices)
        #showImg(canny_edges)
        mask_line = self.__hough_line(canny_edges,vertices)
        res = self.__union (img,mask_line)
        #showImg(res)
        return res

    def principal(self,name):
        return self.__transform_frame(self.img)
        


cap = cv2.VideoCapture('lane1.mp4')    
while(cap.isOpened()):
    ret, img = cap.read()
    if (not ret):
        break
    b = Border(img)
    image = b.principal("hola")
    #transform = transform_frame(img)
    cv2.imshow('frame',image) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
