import tkinter as tk
from Shields.Relays import RaspberryRelay
import json
from Lidar.Machine import MachineObj
from Lidar.LaserDriver import LaserObj

import time


# Callbacks
from CommCallbacks.LdCallbacks import LdCallbacks
from CommCallbacks.ArduinoCallbacks import ArduinoCallbacks
from CommCallbacks.RaspberryCallBacks import RaspberryCallbacks

from Coreiot.Console import Console


class Callback:

    def __init__(self, client, topic, upload_api):
        self.client = client
        self.rpi_console = Console(client, topic, "rpi")
        self.rpi_relays = RaspberryRelay(self.rpi_console)
        self.rpi_callbacks = RaspberryCallbacks(client, topic, self.rpi_relays)
        self.topic = topic

        self.arduino_reply = Console(client, topic, 'ard')
        self.ard = MachineObj('/dev/ttyACM0', self.arduino_reply)   # CORRECT PORT
        self.ard_callbacks = ArduinoCallbacks(client, topic, self.ard)

        self.upload_api = upload_api

        # N2o
        self.ld_n2o_console = Console(client, topic, 'ld/n2o')
        self.ld_n2o = LaserObj("/dev/ttyUSB0", self.ld_n2o_console,'n2o',2500,400,900,50,1)         # CORRECT PORT
        self.ld_n2o_callbacks = LdCallbacks(client, topic  + '/remote/n2o', self.ld_n2o, self.ld_n2o_console, self.ard,self.upload_api)

        # Co2
        self.ld_co2_console = Console(client, topic, 'ld/co2')
        self.ld_co2 = LaserObj("/dev/ttyUSB2", self.ld_co2_console,'co2',2950,2820,3620,45,2)         # CORRECT PORT
        self.ld_co2_callbacks = LdCallbacks(client, topic + '/remote/co2', self.ld_co2, self.ld_co2_console, self.ard,self.upload_api)

        # Ch4
        self.ld_ch4_console = Console(client, topic, 'ld/ch4')
        self.ld_ch4 = LaserObj("/dev/ttyUSB1", self.ld_ch4_console,'ch4',1700,1680,2060,40,3)         # CORRECT PORT
        self.ld_ch4_callbacks = LdCallbacks(client, topic + '/remote/ch4', self.ld_ch4, self.ld_ch4_console, self.ard,self.upload_api)


    def register(self):

        # Raspberry Relay Shields
        self.rpi_callbacks.register()

        # Arduino
        self.ard_callbacks.register()

        # N2o
        self.ld_n2o_callbacks.register()
        #self.n2o_data_callbacks.register()

        # Co2
        self.ld_co2_callbacks.register()
        #self.co2_data_callbacks.register()

        # Ch4
        self.ld_ch4_callbacks.register()
        #self.ch4_data_callbacks.register()

        self.client.message_callback_add(self.topic + "/remote/start", self.auto_measurement)


    def auto_measurement(self, client, topic, message):
        print("============== Start Automated Measurement")
        meas_position=10
        
        self.ard.Relay_toggle(True,'F','f')  #For Fan

        #Door opening /check for time error, 
        while(self.ard.doorstate!=1):
            time.sleep(1)
            self.ard.get_door
            if doorstate=='e':
                reply='Door error'
                break

        #Turn on Components      
        self.ard.start_measure()
        ld_measure(self.ld_n2o)
        Ld_measure(self.ld_co2)
        ld_measure(self.ld_co2)
        self.ard.stop_measure()


        #Go to specified positon and wait for position reply
        self.ard.go_to_position(position)
        position=self.ard.get_position
        while(meas_position+1>=position>=meas_position-1):
            time.sleep(1)
            position=self.ard.get_position
 
        #Turn on Components      
        self.ard.start_measure()
        ld_measure(self.ld_n2o)
        Ld_measure(self.ld_co2)
        ld_measure(self.ld_co2)
        self.ard.stop_measure()

            
        #Door Closing /check for time error, 
        
        while(self.ard.doorstate!=False):
            time.sleep(1)
            self.ard.get_door
            if doorstate=='e':
                reply='Door error'
                break


    def ld_measure(self,ld):
        time.sleep(1)
        self.ard.Relay_toggle(True,'z'+ld.number,ld.number)  #For Fan
        time.sleep(5)
        ld.collect_data(self.ard)
        response = self.upload_api.upload_file(ld.latestdatafile)
        self.console.set("Upload Data {}".format(response))

        self.ard.Relay_toggle(False,'z'+ld.number,ld.number)



        # ------------------------
        # ------------------------
        # ------------------------
        
