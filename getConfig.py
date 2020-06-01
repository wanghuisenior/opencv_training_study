#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: getConfig.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/1 10:44
 @Description:从摄像头框选获取感兴趣区域，并保存最后一帧图片作为依据，同时创建坐标配置文件
"""
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont


def gstreamer_pipeline(
		capture_width=900,
		capture_height=500,
		display_width=960,
		display_height=616,
		framerate=120,
		flip_method=0,
):
	return (
			"nvarguscamerasrc ! "
			"video/x-raw(memory:NVMM), "
			"width=(int)%d, height=(int)%d, "
			"format=(string)NV12, framerate=(fraction)%d/1 ! "
			"nvvidconv flip-method=%d ! "
			"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
			"videoconvert ! "
			"video/x-raw, format=(string)BGR ! appsink"
			% (
				capture_width,
				capture_height,
				framerate,
				flip_method,
				display_width,
				display_height,
			)
	)


drawing = False
ix, iy = -1, -1
mx, my = -1, -1


def draw_rectangle(event, x, y, flags, param):
	global ix, iy, drawing, mx, my
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		ix, iy = x, y
		mx, my = x, y
	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing:  # (ix, iy), (x, y)  (left, top), (right, bottom)
			cv2.rectangle(frame, (ix, iy), (x, y), (0, 255, 0), 2)
	elif event == cv2.EVENT_LBUTTONUP:
		drawing = False
		mx, my = x, y


def cv2ImgAddText(image, text, left, top, textColor=(0, 255, 0), textSize=20):
	if isinstance(image, numpy.ndarray):  # 判断是否OpenCV图片类型
		image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
	draw = ImageDraw.Draw(image)
	font_text = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")
	draw.text((left, top), text, textColor, font=font_text)
	return cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)


# 采集nano csi工业摄像头
# cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
# 采集笔记本自带摄像头
cap = cv2.VideoCapture(0)
cv2.namedWindow('image')
cv2.setMouseCallback("image", draw_rectangle)
while cap.isOpened():
	ok, frame = cap.read()
	if not ok:
		break
	# image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	cv2.waitKey(1)
	cv2.rectangle(frame, (ix, iy), (mx, my), (0, 255, 0), 2)
	img = cv2ImgAddText(frame, "按ENTER保存坐标配置文件", 20, 20, (255, 0, 0), 18)
	cv2.imshow('image', img)
	c = cv2.waitKey(10)
	if c & 0xFF == ord('q'):
		break
	elif c & 0xFF == 13:
		cv2.imwrite("config.jpg", frame)
		with open("coordinate.conf", "w", encoding="utf-8") as f:
			f.write("[left,top] = %s\r[right,bottom] = %s" % (str(ix) + "," + str(iy), str(mx) + "," + str(my)))
			f.close()
		print("saving image 'coordinate.jpg' then generating config file 'coordinate.conf'...")
cap.release()
cv2.destroyAllWindows()
