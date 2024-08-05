# import cv2
from ultralytics import YOLO
# # 加载模型
model = YOLO("yolov10s.pt")
from src.demo.demo import pipeline
import cv2
from flask import Flask, Response

app = Flask(__name__)

# 输入视频流的 URL
stream_url = 'http://172.25.96.195:5000/stream.mjpg'

def generate_frames():
    cap = cv2.VideoCapture(stream_url)

    # 检查视频流是否成功打开
    if not cap.isOpened():
        print("无法打开视频流")
        exit()

    # 获取视频流的宽度和高度
    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 定义视频编解码器和创建 VideoWriter 对象
    # out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (frame_width, frame_height))

    # 计数器
    frame_count = 0
    max_frames = 1e6  # 要保存的帧数

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # 将帧写入视频文件
        # out.write(frame)

        # 编码为 JPEG
        # results = model(frame, verbose=False, conf=0.25, iou=0.6)
        # frame = results[0].plot()
        frame = pipeline(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 发送帧
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        frame_count += 1

    # 释放资源
    # cap.release()
    # out.release()

@app.route('/')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9500)