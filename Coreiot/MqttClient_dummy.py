#!/usr/bin/env python3

import socket
#import paho.mqtt.client as mqtt
from select import select
from time import time
#from Callbacks import Callback
from Lidar_obj import Lidar_obj as Callback
from Coreiot.Upload import Upload

class MqttClient:
    def __init__(self, config):
        self.host = config["mqtt"]["host"]
        self.username = config["mqtt"]["username"]
        self.password = config["mqtt"]["password"]
        self.port = config["mqtt"]["port"]
        self.topic = "life/lidar/" + config["mqtt"]["username"]
        self.upload_api = Upload(config)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
       
        self.callbacks = Callback(self.client, self.topic, self.upload_api)
        self.callbacks.register();

    def on_message(self, client, userdata, message):
        print("message topic=",message.topic)

    def on_log(self, client, userdata, level, buf):
        print("log: ",buf)

    def on_disconnect(self, client, userdata, rc):
        pass

    def disconnect(self):
        pass

    def connect(self):
        pass

    def serve(self, log = False):
        pass
