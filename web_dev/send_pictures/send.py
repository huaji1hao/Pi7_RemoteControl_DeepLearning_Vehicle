import paho.mqtt.client as mqtt
import numpy as np
from PIL import Image
import json
from os import listdir
from os.path import join

PATH = "./images"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected.")
        client.subscribe("Group07/IMAGE/predict")
    else:
        print("Failed to connnect. Error code: ", rc)

def on_message(client, userdata, msg):
    print("Received message from server.")
    resp_dict = json.loads(msg.payload)
    print("Prediction: %s, Score: %3.4f" % (resp_dict["prediction"], float(resp_dict["score"])))

def setup(hostname):
    client = mqtt.Client()
    client.username_pw_set("somya", "trialpass")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()
    return client

def load_image(filename):
    img = Image.open(filename)
    img = img.resize((249, 249))
    imgarray = np.array(img)/255.0
    finl = np.expand_dims(imgarray, axis=0)
    return finl

def send_image(client, filename):
    img = load_image(filename)
    img_list = img.tolist()
    send_dict = {"filename":filename, "data":img_list}
    client.publish("Group07/IMAGE/classify", json.dumps(send_dict))

def main():
    client = setup("172.22.63.91")
    print("Sending data.")
    for file in listdir(PATH):
        send_image(client, join(PATH, file))
    print("Done. Waiting for results")

    while True:
        pass

if __name__ == '__main__':
    main()