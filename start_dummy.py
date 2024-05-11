#!/usr/bin/python3
import paho.mqtt.client as mqtt
import json
import signal 
import sys
from Coreiot.MqttClient import MqttClient

# Load Config
with open('local_conf.json') as confi_file:
    config = json.load(confi_file)

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Connect to Mqqt Broker
client = MqttClient(config)
client.serve(config["mqtt"]["log"])
