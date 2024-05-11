import requests
import html
class Upload:
    def __init__(self, config):
        self.username = config["mqtt"]["username"]
        self.api_key = config["upload"]["api_key"]
        self.url = config["upload"]["url"]
        self.response = ''
    
    def upload_file(self, file_path):
        self.response = ''
        files = {'file': open(file_path,'rb')}
        values = {}
        url = "{}/{}/upload/?api_key={}".format(self.url, self.username, self.api_key)
        print('Upload File :', end="")
        print(file_path)
        self.response = requests.post( url, files=files, data=values).json()
        print(self.response)
         
        return self.response