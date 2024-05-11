from Lidar.LaserDriver import LaserObj
import Lidar.Parameters as d
import json


class RaspberryCallbacks:
    def __init__ (self, client, topic, rpi_relays):
        self.client = client
        self.topic = topic
        self.rpi = rpi_relays

    def register(self):
        self.client.message_callback_add(self.topic+"/remote/rpi/relay/#", self.set_rpi_relays)

    def set_rpi_relays(self, client, topic, message):
        if(message.topic == self.topic + "/remote/rpi/relay/status"):
            print("============== Raspberry Relays Status")    
            self.publish_status()
            return True

        print("============== Raspberry Relays On/Off")    
        payload = json.loads(message.payload.decode("utf-8"))

        if(payload["status"]):
            self.rpi.on(payload["relay"])
        else:
            self.rpi.off(payload["relay"])
        
        self.publish_status()


    def publish_status(self):
        status = self.rpi.get_status()
        payload_string = json.dumps(status, indent=4, sort_keys=True)
        self.client.publish(self.topic + "/status/rpi/relay", payload_string)  