## OPENCV  ——米粒计数

#### 一、项目内容

​         利用opencv-python图像处理库，实现对一幅图片中米粒个数的统计。

​          思路：米粒中心与背景的阈值还是具有很大差别的，但边缘处差别不是很清晰。我们需要分割出米粒的封闭区域并提取其轮廓，对轮廓进行计数即可。轮廓提取方法如下：

​          1、我们可以通过形态学方法将背景分割出来，用原图将背景减去，这样米粒将更加的        清晰，对比度大，方便边缘提取。

​          2、 还可以利用形态学方法将背景和米粒中心制成模板，用原图将模板减去，这样米粒就成了中心挖空的米粒，只留下了外轮廓，我们只需关注其外部形状不是嘛。

#### 二、具体步骤

​         1、 图片读取

​                  先用“文件选择框”读取我们需要处理的RGB图片，并将其转换成灰度图像。

```Python 
import cv2
import os
import tkinter
from tkinter import filedialog

root=tkinter.Tk()  #程序结尾需要添加  root.destroy()
default_dir = r"C:\Users\Administrator\ImageProcess\CountRice"
file_path = filedialog.askopenfilename(title=u'选择图片', initialdir=(os.path.expanduser(default_dir)))
if file_path == None:
    exit()
    
image=cv2.imread(file_path)
img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#灰度化
```
​                                              ![](C:\Users\Administrator\ImageProcess\CountRice\rice.jpg)

​                                                                      img

​          2、制造背景模板，原图与模板进行减操作得到米粒前景

```Python  
#构造模板，10次腐蚀，10次膨胀，得到背景
kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
erosion=cv2.erode(img,kernel,iterations=10)
dilation=cv2.dilate(erosion,kernel,iterations=10)
#原图减去背景得到米粒形状      为什么要减去背景？为了分离出前景，突出分割目标
backImg=dilation
rice=cv2.subtract(img,backImg) 
cv2.imshow("rice",rice)                  
```

![1583837098284](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1583837098284.png)

​     

​          3、二值化

```python
th1 , ret1 = cv2.threshold(rice,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#
cv2.imshow(" ret1", ret1)
```
​                                                    ![1583837224955](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1583837224955.png)  

​        

​               4、轮廓检测

​        这里使用了一个小技巧：仔细观察图片会发现有些米粒是黏在一起的，如何将其分开 呢？由于米粒太小，使用不了分水岭方法，我绞尽脑汁想到了将第一次提取的轮廓用黑色描绘，值得注意的是太小的米粒不能描黑，在这里只将完整大小的米粒轮廓描黑，用于分离。最大颗粒的面积不能太小也不能太大（2个黏在一起要超过170）。

​         然后再进行一次轮廓提取用于计数。

```python
#轮廓检测，并对轮廓描黑，目的是分离米粒，增大间隔
contours,hierarchy=cv2.findContours(ret1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  
#遍历得到最大面积的米粒
maxC=-1
maxS=-1
for cnt in contours:
    tempS=cv2.contourArea(cnt)
    if   tempS<30:
        continue 
    if  maxS<tempS and tempS<170:    #米粒的面积:(30,170)
        maxS=tempS
        maxC=tempC=cv2.arcLength(cnt,True)
        contour=cnt #记录最大米粒的轮廓
    cv2.drawContours(ret1, [cnt], -1, (0, 0, 0), 2)
cv2.imshow(" ret1-b", ret1)
```
![1583838517267](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1583838517267.png)

```python
#提取缩小的米粒二值图像的轮廓，用粉红描绘
contours,hierarchy=cv2.findContours(ret1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
for cnt in contours:
    cv2.drawContours(image, [cnt], -1, (255, 0, 255), 2)  
```

​                                                  ![1583838581230](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1583838581230.png)                                                    

```python
#在img中画出最大面积米粒
cv2.drawContours(image,[contour],-1,(255,0,0),1)
cv2.imshow('image',image)
print(len(contours))
print('面积最大：',maxS)
print('对应米粒周长：',maxC)
cv2.waitKey(0)
root.destroy()

```

![1583838635222](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1583838635222.png)



#### 三、思考

​         最后的结果还是不错的，唯一的遗憾就是有两个米粒连在一起（重叠部分较大），无法分离，暂时未想到办法，想到后补上！！！

​        对于计数，只需要关注物体的形状，甚至是中心即可，将物体看出一个个点分散在图片中。

​        制作掩膜是分离背景、前景很好的办法。

​        形态学腐蚀、膨胀是处理目标物体、分离黏着物体常见的手段之一，物体越大越好分割。