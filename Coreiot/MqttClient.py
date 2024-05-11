#!/usr/bin/env python3

import socket
import paho.mqtt.client as mqtt
from select import select
from time import time
from Callbacks import Callback
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
        
        self.client.subscribe(self.topic + "/remote/#")
        self.client.subscribe(self.topic + "/status/#")

        self.callbacks = Callback(self.client, self.topic, self.upload_api)
        self.callbacks.register();

    def on_message(self, client, userdata, message):
        print("message topic=",message.topic)

    def on_log(self, client, userdata, level, buf):
        print("log: ",buf)

    def on_disconnect(self, client, userdata, rc):
        self.disconnected = True, rc

    def disconnect(self):
        self.client.loop_stop()

    def connect(self):
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.connect(self.host,self.port)

    def serve(self, log = False):
        self.disconnected = (False, None)
        self.t = time()
        self.state = 0

        self.client = mqtt.Client(self.username)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        if(log):
            self.client.on_log = self.on_log

        self.connect()
        self.client.loop_forever()
