import Lidar.Connection as Connection
from serial import Serial
import json
import time

class MachineObj():
    def __init__ (self,serial_address,ard_console):
        #self.serial_address = Serial(serial_address,baudrate=115200, timeout=0.1)
        self.latest_reply = 'none'
        self.ard_console = ard_console

        #Status Variables1
        self.doorstate = ''
        self.fanstate = ''
        self.LD1State = ''
        self.LD2State = ''   
        self.LD3State = ''   
        self.ComponentsState = ''
        self.PSUstate = ''

        self.position = 0.00
        self.temperature=0.0

        #Data Collection
        self.data_running = False
        self.latestdatafile=''
        self.timestamp=[]
        self.data=[]
        
        time.sleep(5)
        #self.get_status()
        

    def open_door(self):
        data = 'D1\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#D1" + reply)

    def close_door(self):
        data = 'D0\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#D0" + reply)


    def move_cw(self, deg = 1): #Rotational movement by x degrees (x is variable)
        data = 'R1' + str(deg) + '\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#CW" + reply)

    def move_ccw(self, deg = 1):  #Rotational movement by x degrees (x is variable)
        data = 'R0' + str(deg) + '\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#CCW" + reply)

    def go_home(self):
        data = 'Rh\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#Rh" + reply)

    def go_to(self):  # Need to take position from field in 0-360 deg range
        data = 'r' + self.Deg_input_field.get() + '\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#r" + reply)

    def go_to_position(self, deg):  # Need to take position from field in 0-360 deg range
        data = 'r' + str(deg) + '\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#r" + reply)


    def fan_toggle(self,state):   # TOGGLE ONLY is enough (Only 'F' serialsend')
        reply = Connection.serialsend(self.serial_address, 'f\n') #gets fanstate    
        while(reply==''):
            reply = Connection.serialsend(self.serial_address, 'f\n') #gets fanstate    
            time.sleep(1)
            if reply!=state:
                reply = Connection.serialsend(self.serial_address, 'F\n')
            print('Toggling')
            
        self.ard_console.set_device(reply, 'rpi')
        self.ard_console.set("#F" + reply)

    def hard_stop(self):
        data = 'S\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device("#HardStop", 'rpi')
        self.ard_console.set("#{}".format(data) + reply)


    def Relay_toggle(self,wanted_state,address,state_quote):   # TOGGLE ONLY is enough (Only 'F' serialsend')
        reply = Connection.serialsend(self.serial_address, state_quote) #gets fanstate
        while(reply==''):
            reply = Connection.serialsend(self.serial_address, state_quote) #gets fanstate
            time.sleep(1)
        if reply!=wanted_state+'\r\n':
            reply = Connection.serialsend(self.serial_address, address)
            print('Toggling')


        self.ard_console.set_device(state_quote, 'rpi')
        self.ard_console.set("#Z" + address + reply)


    def start_LD(self,Ld_number):   # Turn ON LD  #to add to Arduino
        data = 'z'+Ld_number+'\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#Z" + Ld_number + reply)

    def stop_LD(self,Ld_number):   # Turn OFF Components #to add to Arduino
        data = 'z'+Ld_number+'\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#Z" + Ld_number + reply)


    def stop_measure(self):   # Turn OFF Components
        data = 'M0\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#M0" + reply)


    def start_measure(self):    # Turn ON Components
        data = 'M1\n'
        reply = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#M1" + reply)
       
    def get_door(self):
        data='d\n'
        self.doorstate = Connection.serialsend(self.serial_address, data)
        self.doorstate = self.doorstate.replace('\n','').replace('\r','')
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#Door state " + self.doorstate)

    def get_fan(self):
        data='f\n'
        self.fanstate = Connection.serialsend(self.serial_address, data)
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#Fan state " + self.fanstate)

    def get_position(self):
        data='p\n'
        self.position_str = Connection.serialsend(self.serial_address, data)
        self.position_str = self.position_str.replace('\n','').replace('\r','')        
        if self.position_str!='':
            #print(self.position_str)
            #print(self.position_str.encode())
            #print(type(self.position_str))
            self.position=float(self.position_str)
        else:
            self.position=-1       
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#Position " + self.position_str)

    def get_temperature(self):
        data='t\n'
        self.temperature = Connection.serialsend(self.serial_address, data)
        self.temperature = self.temperature.replace('\n','').replace('\r','')
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#Temperature " + self.temperature)  

    def get_relays(self):
        self.LD1State = Connection.serialsend(self.serial_address, '1\n')
        self.LD2State = Connection.serialsend(self.serial_address, '2\n')
        self.LD3State = Connection.serialsend(self.serial_address, '3\n')
        self.ComponentsState = Connection.serialsend(self.serial_address, '4\n')
        self.PSUState = Connection.serialsend(self.serial_address, '5\n')

        data='LD1='+self.LD1State+' - LD2='+self.LD2State+' - LD3='+self.LD3State+' - Comp='+self.ComponentsState+' - PSU='+self.PSUState
        self.ard_console.set_device(data, 'rpi')
        self.ard_console.set("#States: " + data)


    def get_status(self):
        self.get_relays()
        self.get_door()
        self.get_fan()
        self.get_position()
        self.get_temperature()
        self.lia_val=self.read_LIA()


    def read_LIA(self):  ## ONLY ONE TIME, only LIA
        data = 'Ml\n'   #add laserdriver 
        reply = Connection.serialsend_mute(self.serial_address, data)
        reply = reply.replace('\n','').replace('\r','')
        return reply


    def read_Data(self,laserdriver,timestamp):  ## ONLY ONE TIME, All analog data - not used
        data = 'Ms\n'   #add laserdriver 
        reply = Connection.serialsend_mute(self.serial_address, data)
        if len(reply)>5:
            self.timestamp.append(timestamp)         
            self.data.append(reply)

    def refresh_ard(self): # Need to take input from field for full custom serial command, send and receive reply
        reply=Connection.read_serial(self.serial_address)
        print("Reading: ", reply)

    def send(self,command): # Need to take input from field for full custom serial command, send and receive reply
        command = command +'\n'
        reply = Connection.serialsend(self.serial_address, command)
        self.ard_console.set_device(command, 'rpi')
        self.ard_console.set("#M0" + reply)




