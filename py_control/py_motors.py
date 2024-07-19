import serial # 导入用于串口通信的模块
import time

# 初始化串口通信，波特率9600，超时时间1秒
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def send_command(command):
    """发送指令到Arduino, 千万不要修改, 一改就寄"""
    try:
        ser.write((command + '\n').encode('utf-8'))
        response = ser.readline().decode('utf-8').strip()
        if(command == "x"):
            response = "Stop all motors"
        if command != "y":
            print("Received response:", response)
    except serial.SerialTimeoutException:
        print("Write timeout occurred")
    except serial.SerialException as e:
        print("Serial exception occurred:", e)
    except Exception as e:
        print("An unexpected exception occurred:", e)

def stop_motors():
    """停止所有电机"""
    send_command("y")
    send_command('x')

def go_forward(speed, time):
    """前进，指定速度和时间"""
    command = f"f,f,{speed},{time}"
    send_command("y")
    send_command(command)
    
def go_back(speed, time):
    """后退，指定速度和时间"""
    command = f"b,f,{speed},{time}"
    send_command("y")
    send_command(command)

def turn_left(speed, time):
    """左转，指定速度和时间"""
    command = f"l,f,{speed},{time}"
    send_command("y")
    send_command(command)

def turn_right(speed, time):
    """右转，指定速度和时间"""
    command = f"r,f,{speed},{time}"
    send_command("y")
    send_command(command)

def small_go_forward():
    """短暂前进"""
    send_command("y")
    send_command('w')

def small_go_back():
    """短暂后退"""
    send_command("y")
    send_command('s')

def small_turn_left():
    """短暂左转"""
    send_command("y")
    send_command('a')

def small_turn_right():
    """短暂右转"""
    send_command("y")
    send_command('d')

def read_sensors():
    """读取传感器数据"""
    send_command("y")
    command = "read_sensors"
    ser.write((command + '\n').encode('utf-8'))
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            sensor_data = list(map(int, line.split(',')))
            if len(sensor_data) == 3:
                return sensor_data
        except ValueError:
            print("Error parsing sensor data")  # 添加错误处理
            pass
    return None

# 详细使用方法

# 短暂前进
# small_go_forward()

# 短暂后退
# small_go_back()

# 短暂左转
# small_turn_left()

# 短暂右转
# small_turn_right()

# 持续左转，速度200，时间300毫秒
# turn_left(200, 300)

# 持续右转，速度200，时间300毫秒
# turn_right(200, 300)

# 前进，速度100，时间300毫秒
# go_forward(100, 300)

# 一直后退，速度100，python计时0.5秒后停止，有延迟
# go_back(100, -1)
# time.sleep(0.5)
# stop_motors()

# 读取传感器值
sensor_values = read_sensors() # 这个函数返回值是一个数组，可以直接调用
print("Sensor values:", sensor_values[0])
