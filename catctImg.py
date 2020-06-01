#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import sys


def gstreamer_pipeline(
        capture_width=900,
        capture_height=500,
        display_width=960,
        display_height=616,
        framerate=30,
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


# 从摄像头采集一帧视频保存为图片
def getImage(index, path):
    # 采集nano csi工业摄像头
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    # 采集笔记本自带摄像头
    # cap = cv2.VideoCapture(0)
    num = 1
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        # image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            num = num + 1;
            img_name = '%s/%d.jpg' % (path, num)
            print(img_name)
            cv2.imwrite(img_name, frame)
        cv2.imshow('按下键盘C键保存图片到img目录，q键退出', frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    getImage(0, 'img')
