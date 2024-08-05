#!/usr/bin/python3
import time
import cv2
from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder

# 初始化相机
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

# 创建配置，主流和低分辨率流
config = picam2.create_preview_configuration(main={"size": (640, 480)},
                                             lores={"size": (320, 240), "format": "YUV420"})
picam2.configure(config)

# 启动录像
encoder = H264Encoder(10000000)
picam2.start_recording(encoder, "test.h264")

# 录制 10 秒
start_time = time.monotonic()
while time.monotonic() - start_time < 10:
    time.sleep(0.1)  # 简单的延时以保持循环运行

# 停止录像
picam2.stop_recording()
