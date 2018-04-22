import numpy as np
import cv2



def showImg(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)

def ImportantArea(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [vertices], 255)
    n = len(vertices)
    img = cv2.bitwise_and(img,mask)
    for i in range(0,n):
        x,y = vertices[i]
        #name = 'v'+str(i)
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(img,name,(x,y), font, 4,(255,255,0),2,cv2.LINE_AA)
        #showImg(img)
        for j in range(i,n):
            a,b = vertices[j]
            #cv2.line(img, (x, y), (a, b), 255, 5)

    return img

def hough_line (img):
    rho = 1
    theta = np.pi/180
    threshold = 20
    min_line_len = 50
    max_line_gap = 200
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
        minLineLength=min_line_len, maxLineGap=max_line_gap)
    height,width = img.shape
    mask = np.zeros((height,width,3),dtype = np.uint8)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(mask, (x1, y1), (x2, y2), [0,0,255], 5)
    return mask


def union (img, mask):
    return cv2.addWeighted(img, 0.5, mask, 1, 0)

def transform_frame(img):
    
    height,width,_ = img.shape
    v0 = (int(600*width/1000),int(670*height/1000))
    v1 = [int(400*width/1000) , int(670*height/1000)]
    v2 = [int(50*width/1000), height]
    v3 = [int(950*width/1000), height] 

    l_yellow = np.array([20, 100, 100], dtype = np.int8)
    u_yellow = np.array([30, 255, 255], dtype=np.int8)

    vertices = np.array([v0,v1,v2,v3], dtype=np.int32)
    print(vertices)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask_white = cv2.inRange(gray_img,180,255)
    mask_yellow = cv2.inRange(img_hsv, l_yellow, u_yellow)
    mask = cv2.bitwise_or(mask_white, mask_yellow)
    kernel_size = (3,3)
    gauss_gray = cv2.GaussianBlur(mask,kernel_size,0)
    low_threshold = 100
    high_threshold = 200
    canny_edges = cv2.Canny(gauss_gray,low_threshold,high_threshold)
    canny_edges = ImportantArea(canny_edges,vertices)
    #showImg(canny_edges)
    mask_line = hough_line(canny_edges)
    res = union (img,mask_line)
    #showImg(res)
    return res


cap = cv2.VideoCapture('lane3.mp4')

while(cap.isOpened()):
    ret, img = cap.read()
    cv2.imshow('frame',transform_frame(img)) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()