# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 23:18:16 2020

@author: Administrator
"""

import cv2
import os
import tkinter
from tkinter import filedialog

root=tkinter.Tk()
default_dir = r"C:\Users\Administrator\ImageProcess\CountRice"
file_path = filedialog.askopenfilename(title=u'选择图片', initialdir=(os.path.expanduser(default_dir)))
if file_path == None:
    exit()
    
image=cv2.imread(file_path)
img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#构造模板，10次腐蚀，10次膨胀，得到背景
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))#ELLIPSE
erosion=cv2.erode(img,kernel,iterations=10)
dilation=cv2.dilate(erosion,kernel,iterations=10)
#原图减去背景得到米粒形状      为什么要减去背景，为了分离出前景，突出分割目标
backImg=dilation
rice=cv2.subtract(img,backImg) 
cv2.imshow("rice",rice)


#二值化
th1 , ret1 = cv2.threshold(rice,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#
cv2.imshow(" ret1", ret1)

#轮廓检测，并对轮廓描黑，目的是分离米粒，增大间隔
contours,hierarchy=cv2.findContours(ret1, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


#遍历得到最大面积的米粒
maxC=-1
maxS=-1
for cnt in contours:
    tempS=cv2.contourArea(cnt)
    if   tempS<30:
        continue 
    if  maxS<tempS and tempS<170: #米粒的面积:(30,170)
        maxS=tempS
        maxC=tempC=cv2.arcLength(cnt,True)
        contour=cnt  #记录最大米粒的轮廓
    cv2.drawContours(ret1, [cnt], -1, (0, 0, 0), 2)
cv2.imshow(" ret1-b", ret1)
#
#ret1=cv2.GaussianBlur(ret1,(3,3),2)
#ret1=cv2.erode(ret1,kernel,iterations=1)
#cv2.imshow(" ret1-c", ret1)


#提取缩小的米粒二值图像的轮廓，用粉红描绘
contours,hierarchy=cv2.findContours(ret1, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
for cnt in contours:
    cv2.drawContours(image, [cnt], -1, (255, 0, 255), 2)
    
#在img中画出最大面积米粒
cv2.drawContours(image,[contour],-1,(255,0,0),1)
cv2.imshow('image',image)
print(len(contours))
print('面积最大：',maxS)
print('对应米粒周长：',maxC)
cv2.waitKey(0)

root.destroy()
