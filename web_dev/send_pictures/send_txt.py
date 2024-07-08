import requests

def send_text(image_name, result, server_url):
    data = {'filename': image_name, 'result': result}  # 使用指定字段名
    response = requests.post(server_url, data=data)
    print(response.text)

server_url = 'http://172.25.96.195:6000/upload'

image_name = 'ddd'
result = 'cats'

send_text(image_name, result, server_url)
