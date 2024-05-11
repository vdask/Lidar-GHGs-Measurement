from Lidar.LaserDriver import LaserObj
import Lidar.Parameters as d
import json

class LdCallbacks:
    def __init__(self , client, topic, laser_driver, console, machine,upload_api):
        self.client = client
        self.topic = topic
        self.ld = laser_driver
        self.console = console
        self.machine = machine
        self.upload_api = upload_api

    def register(self):
        self.client.message_callback_add(self.topic + "/ld", self.on_n20_ld)
        self.client.message_callback_add(self.topic + "/tec", self.on_n20_tec)
        self.client.message_callback_add(self.topic + "/temp", self.on_n20_temp)
        self.client.message_callback_add(self.topic + "/current", self.on_n20_current)
        self.client.message_callback_add(self.topic + "/init", self.on_n2o_init)
        self.client.message_callback_add(self.topic + "/comm", self.on_n2o_comm)
        self.client.message_callback_add(self.topic + "/ramp", self.set_ramp)
        self.client.message_callback_add(self.topic + "/measurement", self.set_measurement)
        self.client.message_callback_add(self.topic+"/data/collect", self.collect_data)
        self.client.message_callback_add(self.topic+"/data/save", self.save_data)
        

    def set_measurement(self, client, topic, message):
        payload = json.loads(message.payload.decode("utf-8"))
        print("Set Measurement time : {}".format(payload['value']))
        self.ld.update_meas_time(payload["value"])
        self.console.set_device("Measurement Time", 'rpi')
    

# Ramp
    def set_ramp(self, client, topic, message):
        print("============== Ramp") 
        payload = json.loads(message.payload.decode("utf-8"))
        if (payload['action'] == 'update'):
            min = int(payload['min'])
            max = int(payload['max'])
            time = int(payload['time'])
            print("Update Ramp min:{} max:{} time:{}".format(min,max,time))
            self.ld.update_Ramp(min, max, time)
            self.console.set_device("Update Ramp", 'rpi')
        elif (payload['action'] == 'start'):        #not necessary
            print("Start Ramp")
            self.ld.start_Ramp(self.machine)
            self.console.set_device("Start Ramp", 'rpi')
        elif (payload['action'] == 'stop'):         # not necessary
            print("Stop Ramp")
            self.ld.terminate_Ramp()
            self.console.set_device("Stop Ramp", 'rpi')

    def on_n2o_comm(self, client, topic, message):
        print("============== LD Manual Command") 
        payload = json.loads(message.payload.decode("utf-8"))
        self.ld.get_text(payload["com"])

    def on_n2o_init(self, client, topic, message):
        print("============== LD Init") 
        payload = json.loads(message.payload.decode("utf-8"))
        self.ld.LD_status_init()

    def on_n20_temp(self, client, topic, message):
        print("============== Set LD Temp") 
        payload = json.loads(message.payload.decode("utf-8"))
    
        self.ld.set_temperature(payload["value"])

    def on_n20_current(self, client, topic, message):
        print("============== Set LD Current") 
        payload = json.loads(message.payload.decode("utf-8"))
        
        self.ld.set_current(payload["value"])

    def on_n20_ld(self, client, topic, message):
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["status"]):
            print("LD On")
            self.console.set_device("#LD ON ", 'rpi')
            self.ld.setValue(d.LD_State, d.State_Enable)
        else:
            print("LD Off")
            self.console.set_device("#LD OFF", 'rpi')
            self.ld.setValue(d.LD_State, d.State_Disable)

    def on_n20_tec(self, client, topic, message):
        
        print("============== TEC LD") 
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["status"]):
            print("TEC On")
            self.console.set_device("#TEC ON", 'rpi')
            self.ld.setValue(d.TEC_State, d.State_Enable)
        else:
            print("TEC Off")
            self.console.set_device("#TEC OFF", 'rpi')
            self.ld.setValue(d.TEC_State, d.State_Disable)



# Collectors

    def collect_data(self, client, topic, message):
        print("============== Collect Data")
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["status"]):
            print("Start")
            self.ld.collect_data(self.machine)
            self.console.set("Start Collecting Data")
        else:
            print("Terminate")
            self.ld.collect_stop()
            self.console.set("Stop Collecting Data")


    def save_data(self, client, topic, message):
        print("============== Save Data")
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["status"]):
            print("Save & Upload")
            self.ld.save_data()
            response = self.upload_api.upload_file(self.ld.latestdatafile)
            self.console.set("Save & Upload Data {}".format(response))
        else:
            print("Save")
            self.ld.save_data()
            self.console.set("Save Data")