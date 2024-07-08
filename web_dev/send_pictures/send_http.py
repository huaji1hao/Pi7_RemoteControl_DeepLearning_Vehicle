import requests
import datetime

def send_image(file_path, server_url):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    with open(file_path, 'rb') as file:
        files = {'file': (f'{current_time}.jpg', file)}  # 使用当前时间作为文件名
        response = requests.post(server_url, files=files)
        print(response.text)

# server_url = 'http://172.25.96.208:5000/upload'
# server_url = 'http://172.25.96.25:6000/upload'
server_url = 'http://172.25.98.37:5000/upload'

file_path = './images/test.jpg'
send_image(file_path, server_url)
