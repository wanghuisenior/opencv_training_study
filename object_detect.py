#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import sys

################################################》》》》》》》》》》继电器控制部分开始，初始化GPIO模块
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO
# 定义引脚号
output_pin_1 = 31  # J41_BOARD_PIN13---gpio14/GPIO.B06SPI2_SCK/
output_pin_2 = 33  # J41_BOARD_PIN13---gpio14/GPIO.B06/SPI2_SCK
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(output_pin_1, GPIO.OUT)
GPIO.setup(output_pin_2, GPIO.OUT)
################################################》》》》》》》》》》继电器控制部分结束
"""
从csi camera获取视频流进行目标检测
apt-get install python3-pip
python3 -m pip install --upgrade pip
pip3 install numpy
sudo apt install python3-opencv
sudo -H pip3 install opencv-python
"""
# 初始化参数
confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
# 设置输入图片的宽度（inpWidth）和高度（inpHeight）
# 如果想要更快的速度，可以把宽度和高度设置为 320。如果想要更准确的结果，改变他们到 608。   416
inpWidth = 320
inpHeight = 320

# 加载文件
classesFile = "/home/nano64/soft/object_detect/data/ebike2.names"
modelConfiguration = "/home/nano64/soft/object_detect/data/ebike_train2.cfg"
modelWeights = "/home/nano64/soft/object_detect/data/ebike_train2.weights"
# classesFile = "/home/nano64/soft/object_detect/data/coco.names"
# modelConfiguration = "/home/nano64/soft/object_detect/data/yolov3.cfg"
# modelWeights = "/home/nano64/soft/object_detect/data/yolov3.weights"

with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# 读取模型和类别
net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)  # 设置DNN的后端为OpenCV
# net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)  # 目标设置为CPU
# net.setPreferableTarget(cv.dnn.DNN_TARGET_OPENCL)  # 目标设置为GPU， 可能不支持
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawPred(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

    label = '%.2f' % conf
    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                 (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                # 检测到了电动车目标
                # if GPIO.input(output_pin_1) == GPIO.LOW:  # 获取当前状态，并判断当前是否为低电位
                #     GPIO.output(output_pin_1, GPIO.HIGH)  # 如果是低电位则切换为高电位
                #     GPIO.output(output_pin_2, GPIO.HIGH)  # 如果是低电位则切换为高电位
                # else:
                #     pass  # 如果已经是高电位，则不作处理
                print("置信度阈值:", confThreshold, "检测到的目标lable:--" + classes[classId] + "--", "当前置信度:", confidence, )
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
            # else:
            #     if GPIO.input(output_pin_1) == GPIO.HIGH:  # 获取当前状态，并判断当前是否为高电位
            #         GPIO.output(output_pin_1, GPIO.LOW)  # 如果是高电位则切换为低电位
            #         GPIO.output(output_pin_2, GPIO.LOW)  # 如果是高电位则切换为低电位
            #     else:
            #         pass  # 如果已经是高电位，则不作处理

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height)


def gstreamer_pipeline(
        capture_width=900,
        capture_height=500,
        display_width=600,  # 改变输出窗口的大小
        display_height=400,  # 改变输出窗口的大小
        framerate=30,
        flip_method=2):
    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (capture_width,
               capture_height,
               framerate,
               flip_method,
               display_width,
               display_height))


# Process inputs
winName = 'opencv目标检测'
cv.namedWindow(winName)
# 获取摄像头输入流
cap = cv.VideoCapture(0)
# cap = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)
while cv.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))  # 卡顿
    postprocess(frame, outs)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    print(label)
    cv.putText(frame, label, (40, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    cv.imshow(winName, frame)
