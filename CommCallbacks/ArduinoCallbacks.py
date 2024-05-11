from Lidar.LaserDriver import LaserObj
import Lidar.Parameters as d
import json


class ArduinoCallbacks:
    def __init__(self, client, topic, ard_driver):
        self.client = client
        self.topic = topic
        self.ard = ard_driver

    def register(self):
        self.client.message_callback_add(self.topic+"/remote/door/#", self.set_door)
        self.client.message_callback_add(self.topic+"/remote/fan/#", self.set_fan)
        self.client.message_callback_add(self.topic+"/remote/led/#", self.set_led)
        self.client.message_callback_add(self.topic+"/remote/motor/#", self.set_motor)
        self.client.message_callback_add(self.topic+"/remote/measure_components/#", self.set_measure)
        self.client.message_callback_add(self.topic+"/remote/ramp", self.set_ramp)
        self.client.message_callback_add(self.topic+"/remote/stop", self.stop)


    def set_led(self, client, topic, message):
        
        print("============== Led")    
        payload = json.loads(message.payload.decode("utf-8"))
        led = str(payload['led'])

        if(payload["status"]):
            print("Start Led : {}".format(led))
            self.ard.Relay_toggle('1','z'+led+'\n',led+'\n')
            #self.ard.start_LD(led)
        else:
            print("Stop Led : {}".format(led))
            self.ard.Relay_toggle('0','z'+led+'\n',led+'\n')
            #self.ard.stop_LD(led)


    def stop(self, client, topic, message):
        print("============== Hard Stop")
        self.ard.hard_stop()

    def set_ramp(self, client, topic, message):   # APPLIES TO LD CALLBACKS
        print("============== Ramp")
 
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["status"]):
            print("Start/Update Ramp")
            self.ard.update_ramp(payload["v1"], payload["v2"], payload["T"])
        else:
            print("Stop Ramp")
            self.ard.stop_ramp()

    def set_door(self, client, topic, message):
    
        print("============== Door")    
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["status"]):
            print("Open Door")
            self.ard.open_door()
        else:
            print("Close Door")
            self.ard.close_door()

    def set_motor(self, client, topic, message):
            
        print("============== Motor")    
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["action"] == 'cw'):
            print("Move ", end="")
            print(payload["deg"])
            print(" deg cw")
            self.ard.move_cw(payload["deg"])
        elif (payload["action"] == 'ccw'):
            print("Move ", end="")
            print(payload["deg"])
            print(" deg ccw")
            self.ard.move_ccw(payload["deg"])
        elif (payload["action"] == 'position'):
            print("Go To Position ", end="")
            print(payload["deg"])
            self.ard.go_to_position(payload["deg"])
        else:
            print("Go Home")
            self.ard.go_home()

    def set_fan(self, client, topic, message):
        
        print("============== Fan")   
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["status"]):
            print("Start Fan")
            #self.ard.fan_toggle(True)
            self.ard.Relay_toggle('1','F\n','f\n')  #For Fan
        else:
            print("Stop fan")
            #self.ard.fan_toggle(False)
            self.ard.Relay_toggle('0','F\n','f\n')

    def set_measure(self, client, topic, message):
    
        print("============== Measure Components") 
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["status"]):
            print("Start Measure Components")
            self.ard.start_measure()
        else:
            print("Close Measure Compoennts")
            self.ard.stop_measure()