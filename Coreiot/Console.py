
class Console:
    def __init__(self, client, topic, device = ""):
        self.client = client
        self.topic = topic
        self.device =  device

    def set_device(self, value, device):
        self.client.publish(self.topic + "/status/console" + "/" + device, value)  

    def set(self, value):
        self.client.publish(self.topic + "/status/console" + "/" + self.device, value)          