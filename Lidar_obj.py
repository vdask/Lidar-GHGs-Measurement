from Lidar.Machine import MachineObj
from Lidar.LaserDriver import LaserObj
from Lidar.Gui import MainWin as GUI
import Lidar.LidarParameters as L

import Lidar.ch4_parameters as ch4
import Lidar.n2o_parameters as n2o
import Lidar.co2_parameters as co2


import time
import json

import schedule
import threading

from Coreiot.Console_dummy import Console


# Callbacks
from CommCallbacks.LdCallbacks import LdCallbacks
from CommCallbacks.ArduinoCallbacks import ArduinoCallbacks

#from Coreiot.Console import Console
#from Coreiot.MqttClient import MqttClient





class Lidar_obj:

    def __init__(self, client, topic, upload_api,parameters):
        self.client = client
        self.topic = topic

        self.name=parameters.codename

        self.positions=parameters.meas_positions
        self.lasertypes=parameters.lasertypes
        self.meas_duration=parameters.meas_duration
        self.meas_times=parameters.meas_times
         

        self.arduino_reply = Console(client, topic, 'ard')
        self.ard = MachineObj('/dev/ttyACM0', self.arduino_reply)   # CORRECT PORT
        #self.ard = MachineObj('dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Due_Prog._Port_75735303531351405291-if00', self.arduino_reply)   # CORRECT PORT
        
       
        #'/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Due_Prog._Port_75735303531351405291-if00'

        self.ard_callbacks = ArduinoCallbacks(client, topic, self.ard)

        self.upload_api = upload_api


        # N2o
        self.ld_n2o_console = Console(client, topic, 'ld/n2o')
        self.ld_n2o = LaserObj("/dev/ttyUSB0", self.ld_n2o_console,n2o)          # CORRECT PORT
        self.ld_n2o_callbacks = LdCallbacks(client, topic  + '/remote/n2o', self.ld_n2o, self.ld_n2o_console, self.ard,self.upload_api)

        # Co2
        self.ld_co2_console = Console(client, topic, 'ld/co2')
        self.ld_co2 = LaserObj("/dev/ttyUSB2", self.ld_co2_console,co2)    
        self.ld_co2_callbacks = LdCallbacks(client, topic + '/remote/co2', self.ld_co2, self.ld_co2_console, self.ard,self.upload_api)

        # Ch4
        self.ld_ch4_console = Console(client, topic, 'ld/ch4')
        self.ld_ch4 = LaserObj("/dev/ttyUSB1", self.ld_ch4_console,ch4)    
        self.ld_ch4_callbacks = LdCallbacks(client, topic + '/remote/ch4', self.ld_ch4, self.ld_ch4_console, self.ard,self.upload_api)

        #self.ld=self.ld_n2o
        #self.ld=self.ld_co2
        self.ld=self.ld_ch4
        
        #self.laserlist=[self.ld_n2o,self.ld_co2,self.ld_ch4]
        #self.laserlist=[self.ld_n2o,self.ld_ch4]
        self.laserlist=[self.ld_n2o]
        
        #self.gui=GUI(self,self.ard,self.ld,self.client,self.topic)
        #self.gui.mainloop


    def scheduler(self):
        print('Starting scheduler')
        for time_point in self.meas_times:
            #print(time_point)
            schedule.every().day.at(time_point).do(self.auto_measurement)
            #schedule.every().day.at(time_point).do(self.check,time_point)

        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(1)   # 10 sec interval 

        continuous_Schedule_thread = ScheduleThread()
        continuous_Schedule_thread.start()


    def check(self,val):
            print('test sched')
            print(val)


    def register(self):
        # Arduino
        self.ard_callbacks.register()

        # N2o
        self.ld_n2o_callbacks.register()

        # Co2
        self.ld_co2_callbacks.register()

        # Ch4
        self.ld_ch4_callbacks.register()

        self.client.message_callback_add(self.topic + "/remote/start", self.auto_measurement)  #run scheduler



    def auto_measurement(self):
        print("============== Start Automated Measurement")
        time.sleep(1)
        self.ard.Relay_toggle('1','z5\n','5\n')  #For PSU
        time.sleep(1)
        self.ard.Relay_toggle('1','F\n','f\n')  #For Fan
        time.sleep(1)
        self.ard.Relay_toggle('1','z4\n','4\n')  #For Fan
        #self.ard.start_measure() # For Components (LIA,Chopper,PD)
        time.sleep(10)

        #Door opening /check for time error, 
        self.ard.open_door()
        while(self.ard.doorstate!='0'):
            time.sleep(1)
            self.ard.get_door()
            if self.ard.doorstate=='e':
                reply='Door error'
                print(reply)
                break

        # For every position, Go to position (and check if you are there), measure with every laser
        for pos in self.positions:
            time.sleep(2)
            self.ard.go_to_position(pos)
            time.sleep(2)
            self.ard.get_position()

            while(pos+1<=self.ard.position and self.ard.position<=pos-1):
                print('checking pos')
                time.sleep(1)
                start_time = time.time()
                while(self.ard.position==''and start_time-time.time()>60):   # fix time check
                    time.sleep(1)
                    self.ard.get_position()

       
            for laser in self.laserlist:
                time.sleep(1)
                self.gui.machine_update(self.ard)
                print('Starting  a  measure at '+ str(self.ard.position))      
            #Perform measurement   
                self.ld_measure(laser)

        #self.ard.stop_measure() # For Components (LIA,Chopper,PD)
 
        #Door Closing /check for time error, 
        self.ard.close_door()
        while(self.ard.doorstate!='1'):
            time.sleep(1)
            self.ard.get_door()
            if self.ard.doorstate=='e':
                reply='Door error'
                break
            
        self.ard.Relay_toggle('0','z4\n','4\n')   #For Components
        time.sleep(1)
        self.ard.go_home()
        time.sleep(1)
        self.ard.Relay_toggle('0','F\n','f\n')  #For Fan
        time.sleep(1)
        print('End of measurment')
        #self.ard.Relay_toggle('0','z5\n','5\n')  #For PSU


    def ld_measure(self,ld):
        time.sleep(1)
        self.ard.Relay_toggle('1','z'+ld.number+'\n',ld.number+'\n')  #For Fan
        time.sleep(5)
        
        ld.collect_data(self.ard)
        #response = self.upload_api.upload_file(ld.latestdatafile)   # FOR MQTT UPLOAD
        
        #self.console.set("Upload Data {}".format(response))
        self.ard.Relay_toggle('0','z'+ld.number+'\n',ld.number+'\n')



        # ------------------------
        # ------------------------
        # ------------------------
        
if __name__ == '__main__':
    with open('local_conf.json') as confi_file:
        config = json.load(confi_file)

    from Coreiot.MqttClient_dummy import MqttClient
    client = MqttClient(config)

    topic = "Lidar off-grid automation"
    myLidar = Lidar_obj(client,topic,client.upload_api,L)
    #myLidar.gui.mainloop()


