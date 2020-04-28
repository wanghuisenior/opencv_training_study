# -*- coding:utf8 -*-
import os
import cv2  # 请确保已经安装了opencv-python ， pip install openc-python

# 测试图片
imgName = "w.jpg"
# 训练得到的分类器xml文件，训练完成后在trained_classifiers文件夹下，即：params.xml
# xmlFileName = "cascade.xml"
xmlFileName = "haarcascade_frontalface_alt.xml"
if not (os.path.exists(imgName) and os.path.exists(xmlFileName)):
    print("图片或检测器文件不存在")
# 矩形颜色和描边
color = (0, 0, 255)  # 红色框
strokeWeight = 1  # 线宽为 1

# 测试训练的检测器是否可用
windowName = "object detect"
img = cv2.imread(imgName)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 加载检测文件
cascade = cv2.CascadeClassifier(xmlFileName)

rects = cascade.detectMultiScale(gray)
if len(rects) > 0:
    print('========================检测到%d个目标===============================' % (len(rects)))
else:
    print('没检测到东西')
# 获取矩形列表
for x, y, width, height in rects:
    cv2.rectangle(img, (x, y), (x + width, y + height), color, strokeWeight)

# 显示
cv2.imshow(windowName, img)
cv2.waitKey(0)
