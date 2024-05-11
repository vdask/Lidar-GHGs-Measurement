import Lidar.Parameters as d
import Lidar.Connection as Connection
import time
import datetime as dt
from pathlib import Path


from serial import Serial

#import Lidar.Ramp_thread as Ramp_thread

class LaserObj():
    def __init__(self,serial_address,console,laser_type):
        #self.serial_address = Serial(serial_address,baudrate=115200, timeout=0.05)
        self.laser_type = laser_type
        self.console = console
        self.variable_int(laser_type)


        #DATA ACQ Variables
        self.running = False
        self.timestamp=[]
        self.LIA=[]
        self.LD_curr=[]
        self.LD_temp=[]
        self.latestdatafile=''
        self.meas_time_start=0

  
        # Laser Driver Status Variables 
        #  // need to add : Max_LD_current, Max TEC Current
    def variable_int(self,laser_type):
        self.RampMin = laser_type.RampMin
        self.RampMax = laser_type.RampMax
        self.RampTime = laser_type.RampTime
        self.number= laser_type.number
        self.max_tec_current_limit = laser_type.max_tec_current_limit
        self.max_current_limit = laser_type.max_current_limit
        self.a=(self.RampMax-self.RampMin)/self.RampTime
        self.prev=0
        self.measurement_duration = laser_type.duration
        self.name = laser_type.name
        self.readOut=''
        self.Error_reply=''
        self.Temperature=laser_type.Temperature
        self.default_current=laser_type.default_current
        self.LD_state=False
        self.Current_Set=''
        self.LD_Enable=''
        self.Ext_NTC_interlock=''
        self.Interlock=''
        self.Lock_Interlock=False
        self.Lock_OverCurrent=False
        self.Lock_OverHeat=False
        self.Lock_ExtNTCInterlock=False
        self.Lock_TECError=False
        self.Lock_TEC_selfHeat=False
        self.TEC_state=False
        self.Temp_set=''
        self.TEC_Enable=''
        #self.rampcount=0
        #self.ramps=[]


    def start_Ramp(self,machine): # Start ramp and Data Acq
        self.collect_data(machine)
        
        #self.ramp=Ramp_thread.Ramp_thread()
        #self.ramp.start_Ramp(self.RampMin,self.RampMax,self.RampTime,self,machine)
   

    def collect_data(self,machine):
        # Driver initialization, TEC ON and LD ON
        self.LD_status_init()
        time.sleep(2)
        self.setValue(d.TEC_State, d.State_Enable)
        time.sleep(2)
        self.setValue(d.LD_State, d.State_Enable)
        time.sleep(0.1)
        self.console.set('Init -OK , TEC & LD On')
        time.sleep(2)
        #Collect Data
        self.collect_process(machine)
        time.sleep(2)
        self.console.set('Collect Complete')
        time.sleep(2)
        # Save Data
        self.save_data(machine.position)
        # Turn off LD
        time.sleep(2)
        self.setValue(d.LD_State, d.State_Disable)
        time.sleep(2)
        self.setValue(d.TEC_State, d.State_Disable)
        self.console.set('Systems Off')


    def collect_process(self,machine):
        self.clear_Data()
        self.running = True
        print("Measurement Start time: {}".format(self.measurement_duration))

        self.meas_time_start = time.time()
        measure_time=0
        #self.rampcount=0
        #self.ramps=[]
        start_time = time.time()
        
        i=0
        while(self.measurement_duration>measure_time-self.meas_time_start and self.running==True):
            # Need Regulart Timestamp for CoreIoT Charts
            measure_time = time.time();
            
            timestamp = measure_time - start_time
            timestamp = float("%0.4f" % (timestamp))
                   
            #DATA Acquisition
            self.timestamp.append(measure_time)
            self.LIA.append(machine.read_LIA())
            self.LD_curr.append(self.getCurrent())
            self.LD_temp.append(self.getTemp())
            #self.ramps.append(self.rampcount)


            i+=1
            print(i,timestamp,self.LIA[-1],self.LD_curr[-1],self.LD_temp[-1])
            
            if (timestamp>=self.RampTime) :    #restart after period T
                start_time = time.time()
                self.val=self.RampMin
                #self.rampcount+=1
                print('Ramp Period',timestamp)
   

            # Check value, based on Ramp line equation
            self.val=int(timestamp*self.a+self.RampMin)  

            # Check to see if val is changed from previous step
            if (self.val!=self.prev):
                self.prev=self.val
                value = format(self.val,'04X') 
                command = 'P' + d.LD_CurrentVal + ' ' + value + '\r'
                self.serial_address.write(command.encode())
                i=0

        # Measurement and Ramp Functions
    def collect_stop(self):   # terminates Ramp and Data Aacq
        if(hasattr(self, 'ramp')):
            self.running = False        

    def update_Ramp(self,RampMin,RampMax,RampTime):  # Need to have dedicated key
        self.RampMin=RampMin
        self.RampMax=RampMax
        self.RampTime=RampTime

    def update_meas_time(self,meas_time):  # Need to have dedicated key
        self.measurement_duration=meas_time




    def save_data(self,position):
        now=dt.datetime.now()
        name=self.name + '_p'+str(position)+'_' + now.strftime("%H-%M-%S") +'.csv'
        

        # Save data in sub folders based on measurement date
        folder = "data/" + str(dt.datetime.now().year) + "/" + str(dt.datetime.now().month) + "/" + str(dt.datetime.now().day) + "/"
        Path(folder).mkdir(parents=True, exist_ok=True)
        
        self.latestdatafile=folder + name

        with open(self.latestdatafile, 'w') as filehandle:
            filehandle.write('{},{},{},{}\n'.format('timestamp','ld_current','ld_temp',self.name))
            for (listitem,listitem2,listitem3,listitem4) in zip(self.timestamp,self.LD_curr,self.LD_temp,self.LIA):
                filehandle.write('{},{},{},{}\n'.format(listitem,listitem2,listitem3,listitem4))
        print('Data saved')


    def clear_Data(self):
        self.timestamp=[]
        self.LIA=[]
        self.LD_curr=[]
        self.LD_temp=[]


    # Communication Functions
    def setValue(self, parameter, setvalue):  # Sets value according to parameter and value input
        value = parameter
        parameter = 'P' + parameter + ' ' + setvalue + '\r'
        self.readOut = Connection.serialsend(self.serial_address, parameter)
        self.getValue(value)
        self.console.set(self.readOut)
        return self.readOut

    def getValue(self, parameter):  # Gets value according to parameter
        parameter = 'J' + parameter + '\r'
        self.readOut = Connection.serialsend(self.serial_address, parameter)
        self.update_state_variables(self.readOut)
        self.console.set(self.readOut)
        return self.readOut


    def getCurrent(self):  # Gets LD Current according to parameter
        parameter = 'J' + d.LD_CurrentMeas + '\r'
        rep = Connection.serialsend_mute(self.serial_address, parameter)
        val=-1
        if rep[0] == 'K':
            address=rep[1:5]
            val=bin(int(rep[6:10], 16))[2:].zfill(8)
            if address == d.LD_CurrentMeas:
                val=int(rep[5:10],16)/10
        else:
            val=-1       
        return val


    def getTemp(self):  # Gets Temperature according to parameter
        parameter = 'J' + d.TEC_Meas + '\r'
        rep = Connection.serialsend_mute(self.serial_address, parameter)
        address=rep[1:5]
        val=-1
        if rep[0] == 'K':       
            val=bin(int(rep[6:10], 16))[2:].zfill(8)
            if address == d.TEC_Meas:
                val=int(rep[5:10],16)/100
        else:
            val=-1
        return val


    def refresh_status(self):  # Refresh info for LD driver state, TEC state, and Lock status
        self.Temperature=self.getTemp()
        self.LD_current=self.getCurrent()
        self.readOut = Connection.read_serial(self.serial_address)
        self.update_state_variables(self.readOut)
        self.console.set(self.readOut)
        return self.readOut

    def LD_status_init(self):  # Sets LD drivers and TEC wanted states
        # self.serial_adress=serial.Serial(self.comport,baudrate=115200, timeout=0.2)
        self.setValue(d.LD_State, d.State_IntEn)  # LD enable - Internal
        # self.setValue(d.LD_State,d.State_ExtSet)  # Current set - External
        self.setValue(d.LD_State, d.State_IntSet)  # Current set - Internal

        self.setValue(d.TEC_State, d.State_IntEn)  # TEC enable - Internal
        self.setValue(d.TEC_State, d.State_IntSet)  # Temperature set - Internal
        
        self.setValue(d.LD_State, d.Deny_Inter)  # Interlock - Denied
        self.setValue(d.LD_State, d.Deny_ext_NTC_Inter)  # External Interlock NTC - Denied

        self.set_current(self.default_current)       # Set specified Default-Measurment Current
        self.set_temperature(self.Temperature) # Set specified Default-Measurment Temperature
        self.set_current_limit(self.max_current_limit)
        self.set_tec_current_limit(self.max_tec_current_limit)

        self.getValue(d.Lock_Status)


    def set_temperature(self,value):  # takes values from 0-4200 (in 0.01 deg Celcius), converts to HEX
        value = int(value)
        value = format(value, '04X')
        self.readOut = self.setValue(d.TEC_Val, value)
        self.console.set_device("#Set Temp" + str(value) , 'rpi')
        self.console.set(self.readOut)
        return self.readOut

    def set_current(self,value):    # takes values from 0-7500 (in 0.1 mA), converts to HEX- we have a max limit per Laser Driver
        value = int(value)
        value = format(value, '04X')
        self.readOut = self.setValue(d.LD_CurrentVal, value)
        self.console.set_device("#Set Current " + str(value), 'rpi')
        self.console.set(self.readOut)
        return self.readOut

    def set_current_limit(self,value):
        value = int(value)
        value = format(value, '04X')
        self.readOut = self.setValue(d.LD_CurrentMax_lim, value)
        self.console.set_device("#Set Current Max Lim " + str(value), 'rpi')
        self.console.set(self.readOut)
        return self.readOut


    def set_tec_current_limit(self,value):
        value = int(value)
        value = format(value, '04X')
        self.readOut = self.setValue(d.Tec_Curr_Lim, value)
        self.console.set_device("#Set Tec Current Max Lim " + str(value), 'rpi')
        self.console.set(self.readOut)
        return self.readOut
    

    def update_state_variables(self,reply):
        rep=reply
       
        if(len(rep) == 0) :
            rep=' '

        #rep='K0A15 00C1'
        address=rep[1:5]
        scale = 16 ## equals to hexadecimal
        num_of_bits = 8

        if rep == 'K0000 0000':
            self.Error_reply=rep
        
        if rep[0] == 'E':
            self.Error_reply=rep


        elif rep[0] == 'K':
            value=bin(int(rep[6:10], 16))[2:].zfill(8)
            
            if address == d.TEC_Meas:
                value=int(rep[5:10],16)/10
                self.Temperature=value

            if address == d.LD_CurrentMeas:
                value=int(rep[5:10],16)/10
                self.LD_current=value
           
            
            elif address == d.LD_State:

                if value[-2] == '0':
                    self.LD_state=False
                else:
                    self.LD_state=True

                if value[-3] == '0':
                    self.Current_Set='Ext'
                else:
                    self.Current_Set='Int'

                if value[-5] == '0':
                    self.LD_Enable='Ext'
                else:
                    self.LD_Enable='Int'

                if value[-7] == '0':
                    self.Ext_NTC_interlock='Allowed'
                else:
                    self.Ext_NTC_interlock='Denied'

                if value[-8] == '0':
                    self.Interlock='Allowed'
                else:
                    self.Interlock='Denied'



            elif address == d.Lock_Status:

                if value[-2] == '1':
                    self.Lock_Interlock=True
                else:
                    self.Lock_Interlock=False

                if value[-4] == '1':
                    self.Lock_OverCurrent=True
                else:
                    self.Lock_OverCurrent=False

                if value[-5] == '1':
                    self.Lock_OverHeat=True
                else:
                    self.Lock_OverHeat=False

                if value[-6] == '1':
                    self.Lock_ExtNTCInterlock=True
                else:
                    self.Lock_ExtNTCInterlock=False

                if value[-7] == '1':
                    self.Lock_TECError=True
                else:
                    self.Lock_TECError=False

                if value[-8] == '1':
                    self.Lock_TEC_selfHeat=True
                else:
                    self.Lock_TEC_selfHeat=False


            elif address == d.TEC_State:
            
                if value[-2] == '0':
                    self.TEC_state=False
                else:
                    self.TEC_state=True

                if value[-3] == '0':
                    self.Temp_set='Ext'
                else:
                    self.Temp_set='Int'

                if value[-5] == '0':
                    self.TEC_Enable='Ext'
                else:
                    self.TEC_Enable='Int'

        else:
                 print("Nothing")


    def get_text(self,com):  # sends manual serial communication
        #com = self.serial_send.get() + '\r'
        self.readOut = Connection.serialsend(self.serial_address, com)
        self.auto_response(com)
        self.update_state_variables(self.readOut)
        self.console.set(self.readOut)


    def auto_response(self, com):
        if com[0] == 'P':
            num_of_the_parameter = com[1:5]
            self.getValue(num_of_the_parameter)


    def disconnect_LD(self):
        time.sleep(2)
        self.setValue(d.LD_State, d.State_Disable)
        time.sleep(2)
        self.setValue(d.TEC_State, d.State_Disable)
        #self.serial_address.close()



    def connect_LD(self):
        self.serial_address.open()









