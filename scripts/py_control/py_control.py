from flask import Flask, request, render_template, jsonify
import serial
import signal
import sys
import cv2
import time
from picamera2 import Picamera2, Preview, MappedArray
import requests
import datetime
import sqlite3
from flask import Flask, request
import serial
import time
import io
import logging
import socketserver
from http import server
import threading
from threading import Condition
import os
from shutil import copyfile
import heapq
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput

# Initialize serial connection to Arduino
app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
flag = 0

from py_motors import * # 可以直接用py_motors里面的函数，不需要声明
from trialmap import * # 直接使用trialmap里面的函数dijstra
from get_distance import *

# 返回值是distance大小，直接调用即可
def get_distance_from_server():
    try:
        response = requests.get('http://0.0.0.0:6000/get_distance')
        if response.status_code == 200:
            data = response.json()
            if 'distance' in data:
                return data['distance']
            else:
                print("Distance value not found in response")
        else:
            print(f"Failed to get distance: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

# 输出结果，0直行，1右转，3左转
def path_to_instructions(path_list):
    instructions = []
    global flag

    for i in range(0, len(path_list)):
        inst = (path_list[i] + flag) % 4
        if inst == 1:
            flag -= 1
        elif inst == 3:
            flag += 1
        instructions.append(inst)

    return instructions

# 示例用法
# path_list = [3, 2, 1, 0]
# instruction_list = path_to_instructions(path_list)
# print(instruction_list)  # 输出应当为 [3, 3, 3, 3], 即四次左转



# 模拟输入开始点和结束点
# start = int(input("Enter the start vertex (0-14): "))
# end = int(input("Enter the end vertex (0-14): "))
# # path_list是形如[3,2,1,0]的数组
# path_list = run_dij(start, end)
# print(path_list)



# 控制逻辑
# def control_car(current_path):
#     if current_path is not None:
#         # sensor_data = read_sensors() # 每次使用前读取
#         # 直接使用sensor_data[0]...
#         if sensor_data[0] == 1 and sensor_data[2] == 0:
#             # 左传感器检测到黑线
#             stop_motors()
#             time.sleep(0.5)
#             turn_left(2,50)
#             go_forward(2,-1)
#         elif sensor_data[0] == 0 and sensor_data[2] == 1:
#             # 右传感器检测到黑线
#             stop_motors()
#             time.sleep(0.5)
#             turn_right(2, 50)
#             send_command(GO_FORWARD)
#         elif :junc_dis < 120:
#             # 左右传感器都检测到黑线
#             stop_motors()
#             time.sleep(0.5)
#          if sensor_data[0] == 1 and sensor_data[2] == 1:
#             JUDEGmotor()                                          #TO DO!!!!!!!!!!!!路径选择判断
#         else:
#             stop_motors()
#     elif current_path is not None:
#         if sensor_data[0] == 0 and sensor_data[2] == 0:
#               go_forward(2,-1)


# print(get_distance_from_server())





        