from flask import Flask, request
import serial
import threading
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
app = Flask(__name__)

last_sent_time = 0

def send_to_arduino(distance_str):
    global last_sent_time
    try:
        current_time = time.time()
        if current_time - last_sent_time >= 0.5:
            ser.write(('D' + distance_str + '\n').encode('utf-8'))
            print("Data sent to Arduino")
            # 尝试读取返回数据，以清空缓存
            response = ser.readline().decode('utf-8').strip()
            print("Received response:", response)
            last_sent_time = current_time
        else:
            print("Skipping send due to rate limit")
    except serial.SerialTimeoutException:
        print("Write timeout occurred")
    except serial.SerialException as e:
        print("Serial exception occurred:", e)
    except Exception as e:
        print("An unexpected exception occurred:", e)

@app.route('/upload', methods=['POST'])
def upload_string():
    print("Request form keys:", request.form.keys())
    if 'distance' not in request.form:
        print("Checking JSON data")
        data = request.get_json()
        if not data or 'distance' not in data:
            print("Missing distance key")
            return 'Missing distance', 400
        distance = data['distance']
    else:
        distance = request.form['distance']
    
    if distance == '':
        print("Distance is empty")
        return 'Distance is empty', 400
    
    # 假设你还有后续处理逻辑
    print("Received distance:", distance)
    distance_str = str(distance)

    # 异步处理串口写入
    threading.Thread(target=send_to_arduino, args=(distance_str,)).start()

    return 'Text successfully received and sent', 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
