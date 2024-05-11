import tkinter as tk
import Lidar.Machine as Machine
import Lidar.LaserDriver as LaserDriver
import Lidar.Parameters as d
import Lidar.Graph as Graph

import time


class MainWin(tk.Tk):
    def __init__(self,controller,machine,laserdriver,client,topic):
        #super().__init__()
        tk.Tk.__init__(self)
        self.title("CherryLidar")

        self.controller=controller
        self.ard=machine
        self.ld=laserdriver



        self.frames = {}
        self.Machine_States(0,0)
        self.MachineWidgets(0,1)

        self.LD_States(0,3)
        self.DataInterface(2,0)

        #self.RampInterface(0,2)

        self.LD_Select(1,0)
        self.LaserWidgets(1,1)
  
          
        #time.sleep(1)
        #self.machine_update(self.ard)


        
    def MachineWidgets(self,x,y):
        self.MachineFrame = tk.Frame(self,relief="ridge",bd=2,bg="gray")
        self.MachineFrame.grid(row=x,column=y,sticky='news')

        self.Open_Door_button = tk.Button(self.MachineFrame, text='Open Door', fg='black', bd=3, relief='raised', command=lambda:self.ard.open_door())
        self.Open_Door_button.grid(row=x, column=y, sticky='N', padx=20, pady=10)

        self.Close_Door_button = tk.Button(self.MachineFrame, text='Close Door', fg='black', bd=3, relief='raised', command=lambda:self.ard.close_door())
        self.Close_Door_button.grid(row=x+1, column=y, sticky='N', padx=20, pady=10)

        self.Fan_button = tk.Button(self.MachineFrame, text='Fan Toggle', fg='black', bd=3, relief='raised', command=lambda:self.ard.fan_toggle(not self.ard.fanstate))
        self.Fan_button.grid(row=x+2, column=y+2, sticky='N', padx=20, pady=10)

        self.Deg_input_field = tk.Entry(self.MachineFrame, width=12)
        self.Deg_input_field.grid(row=x+1, column=y+1, padx=20, pady=10)
         
        self.Move_CW_button = tk.Button(self.MachineFrame, text=' MoveCW ', fg='black', bd=3, relief='raised', command=lambda:self.ard.move_cw())
        self.Move_CW_button.grid(row=x, column=y+2, sticky='N', padx=20, pady=10)

        self.Move_CCW_button = tk.Button(self.MachineFrame, text='MoveCCW', fg='black', bd=3, relief='raised', command=self.ard.move_ccw)
        self.Move_CCW_button.grid(row=x+1, column=y+2, sticky='N', padx=20, pady=10)

        self.Refresh_Button = tk.Button(self.MachineFrame, text='Refresh Status', fg='black', bd=3, relief='raised',command=lambda: self.machine_update(self.ard))
        self.Refresh_Button.grid(row=x+2, column=y+1, sticky='N', padx=20, pady=10)
        
        #self.arduino_entry = tk.Entry(self.MachineFrame, textvariable=self.arduino_rep)
        #self.arduino_entry.grid(row=x+2, column=y)
        
        self.serial_button = tk.Button(self.MachineFrame, text='SEND', fg='black', bd=3, relief='raised',command=lambda: self.ard.send(self.arduino_send.get()))
        self.serial_button.grid(row=x+3, column=y+1, sticky='N', padx=20, pady=10)

        self.arduino_send = tk.StringVar()
        self.arduino_send = tk.Entry(self.MachineFrame,textvariable=self.arduino_send)
        self.arduino_send.grid(row=x+3, column=y, padx=20, pady=10)

        self.arduino_reply = tk.StringVar()
        self.arduino_reply.set("Arduino Response")

        self.LD_Serial_Reply = tk.Entry(self.MachineFrame, textvariable=self.arduino_reply)
        self.LD_Serial_Reply.grid(row=x+2, column=y, padx=20, pady=10)

        self.Goto_button = tk.Button(self.MachineFrame, text='GoTo', fg='black', bd=3, relief='raised', command=lambda:self.ard.go_to_position(self.Deg_input_field.get()))
        self.Goto_button.grid(row=x, column=y+1, sticky='S', padx=20, pady=10)
        
        self.Stop_Rot_button = tk.Button(self.MachineFrame, text='STOP', fg='red', height=2, width=16, command=lambda:self.ard.hard_stop())
        self.Stop_Rot_button.grid(row=x, column=y+3, sticky='NESW',rowspan=3)

        self.Component_On_button = tk.Button(self.MachineFrame, text='Components On', fg='black', bd=3, relief='raised', command=lambda: self.ard.Relay_toggle('1','z4\n','4\n'))
        self.Component_On_button.grid(row=x+4, column=y+3, padx=0, pady=0, sticky='senw')

        self.Component_Off_button = tk.Button(self.MachineFrame, text='Components Off', fg='black', bd=3, relief='raised', command=lambda: self.ard.Relay_toggle('0','z4\n','4\n'))
        self.Component_Off_button.grid(row=x+5, column=y+3, padx=0, pady=0, sticky='senw')

        self.LD1_on_button = tk.Button(self.MachineFrame, text='LD1 On - N2O', fg='black', bd=3, relief='raised', command=lambda: self.ard.Relay_toggle('1','z1\n','1\n'))
        self.LD1_on_button.grid(row=x+4, column=y, padx=0, pady=0, sticky='senw')
                    
        self.LD2_on_button = tk.Button(self.MachineFrame, text='LD2 On - CO2', fg='black', bd=3, relief='raised', command=lambda: self.ard.Relay_toggle('1','z2\n','2\n'))
        self.LD2_on_button.grid(row=x+4, column=y+1, padx=0, pady=0, sticky='senw') 
        
        self.LD3_on_button = tk.Button(self.MachineFrame, text='LD3 On - CH4', fg='black', bd=3, relief='raised', command=lambda: self.ard.Relay_toggle('1','z3\n','3\n'))
        self.LD3_on_button.grid(row=x+4, column=y+2, padx=0, pady=0, sticky='senw') 

        self.LD1_off_button = tk.Button(self.MachineFrame, text='LD1 Off - N2O', fg='black', bd=3, relief='raised', command=lambda: self.ard.Relay_toggle('0','z1\n','1\n'))
        self.LD1_off_button.grid(row=x+5, column=y, padx=0, pady=0, sticky='senw')
                    
        self.LD2_off_button = tk.Button(self.MachineFrame, text='LD2 Off - CO2', fg='black', bd=3, relief='raised', command=lambda: self.ard.Relay_toggle('0','z2\n','2\n'))
        self.LD2_off_button.grid(row=x+5, column=y+1, padx=0, pady=0, sticky='senw') 
        
        self.LD3_off_button = tk.Button(self.MachineFrame, text='LD3 Off - CH4', fg='black', bd=3, relief='raised', command=lambda: self.ard.Relay_toggle('0','z3\n','3\n'))
        self.LD3_off_button.grid(row=x+5, column=y+2, padx=0, pady=0, sticky='senw') 
        

    def LaserWidgets(self,x,y):
        self.LaserFrame = tk.Frame(self,relief="ridge",bd=2,bg="gray")
        self.LaserFrame.grid(row=x,column=y,columnspan=2,sticky='news')

        self.LD_Serial_Send_button = tk.Button(self.LaserFrame, text='SEND', fg='black', bd=3, relief='raised', command=lambda: self.ld.get_text(self.serial_reply))
        self.LD_Serial_Send_button.grid(row=x+2, column=y+1, sticky='N', padx=20, pady=10)

        self.LD_Refresh_Button = tk.Button(self.LaserFrame, text='Refresh Status', fg='black', bd=3, relief='raised', command=lambda: self.parse_reply(self.ld))
        self.LD_Refresh_Button.grid(row=x+6, column=y+2, sticky='N', padx=20, pady=10)

        self.LD_Initialize_button = tk.Button(self.LaserFrame, text='Initialize', fg='black', bd=3, relief='raised', command =lambda: self.ld.LD_status_init())
        self.LD_Initialize_button.grid(row=x+6, column=y, sticky='N', padx=20, pady=10)

        self.LD_Off_Button = tk.Button(self.LaserFrame, text='LD OFF', fg='red', bd=3, relief='raised', command=lambda: self.ld.setValue(d.LD_State, d.State_Disable))
        self.LD_Off_Button.grid(row=x+1, column=y, sticky='N', padx=20, pady=10)

        self.LD_On_button = tk.Button(self.LaserFrame, text='LD ON', fg='green', bd=3, relief='raised', command = lambda: self.ld.setValue(d.LD_State, d.State_Enable))
        self.LD_On_button.grid(row=x, column=y, sticky='N', padx=20, pady=10)

        self.TEC_On_button = tk.Button(self.LaserFrame, text="TEC ON", fg='green', bd=3, relief='raised', command = lambda: self.ld.setValue(d.TEC_State, d.State_Enable))
        self.TEC_On_button.grid(row=x, column=y+1,sticky='N', padx=20, pady=10)

        self.TEC_Off_Button = tk.Button(self.LaserFrame, text='TEC OFF', fg='red', bd=3, relief='raised',command = lambda: self.ld.setValue(d.TEC_State, d.State_Disable))
        self.TEC_Off_Button.grid(row=x+1, column=y+1,padx=20, pady=10, sticky='n')

        self.serial_send = tk.StringVar()
        self.LD1_send = tk.Entry(self.LaserFrame, textvariable=self.serial_send)
        self.LD1_send.grid(row=x+2, column=y)

        self.serial_reply = tk.StringVar()
        self.serial_reply.set("Waiting for Response")

        self.LD1_reply = tk.Entry(self.LaserFrame, textvariable=self.serial_reply)
        self.LD1_reply.grid(row=x+3, column=y+0)


        self.Disconnect_button = tk.Button(self.LaserFrame, text="Disconnect LD Driver", bd=3, relief='raised',command = lambda: self.ld.disconnect_LD())
        self.Disconnect_button.grid(row=x+6, column=y+1, padx=20, pady=10, sticky='n')

        self.temp_field = tk.StringVar()
        self.temp_field.set(" °C")

        self.Temp_field = tk.Entry(self.LaserFrame, textvariable=self.temp_field, width=12)
        self.Temp_field.grid(row=x+4, column=y+1, padx=0, pady=10,sticky='w')

        self.Set_Temp_Button = tk.Button(self.LaserFrame, text='SET Temp °C',command = lambda: self.ld.set_temperature(self.temp_field.get()))
        self.Set_Temp_Button.grid(row=x+4, column=y, padx=0, pady=0,sticky='we')

        
        self.LD_Current_Button = tk.Button(self.LaserFrame,text = 'SET LD Current', command = lambda: self.ld.set_current(self.ld_current_field.get()))
        self.LD_Current_Button.grid(row=x+5, column=y, padx=0, pady=10, sticky='we')

        self.ld_current_field = tk.StringVar()
        self.LD_field = tk.Entry(self.LaserFrame, textvariable=self.ld_current_field, width =10)
        self.LD_field.grid(row=x+5,column=y+1,sticky='w')


    def ld_toggle(self,laserdriver):
        self.ld.disconnect_LD()   #Turns off LD,TEC and serial port
        #self.ard.Relay_toggle('0','z'+self.ld.number+'\n',self.ld.number+'\n')  #Turns off PSU
        self.ld=laserdriver
        #self.ld.connect_LD()

 

    def LD_Select(self,x,y):  # Draws buttons ,etc.
        self.LD_SelectFrame = tk.Frame(self,relief="ridge",bd=2,bg="gray")
        self.LD_SelectFrame.grid(row=x,column=y,sticky='news')

        self.LD_Label = tk.Label(self.LD_SelectFrame, text="Laser Driver Selection", height=1, fg='Azure', background='#303030')
        self.LD_Label.grid(row=x, column=y,columnspan=3, sticky='news')

        self.CO2_LD_button = tk.Button(self.LD_SelectFrame, text='C02', fg='black', bd=3, relief='raised',
                                       command=lambda: self.ld_toggle(self.ld_co2))
        self.CO2_LD_button.grid(row=x+1, column=y+1, padx=0, pady=10)

        self.N2O_LD_button = tk.Button(self.LD_SelectFrame, text='N20', fg='black', bd=3, relief='raised',
                                       command=lambda:  self.ld_toggle(self.ld_n2o))
        self.N2O_LD_button.grid(row=x+1, column=y, padx=0, pady=10)

        self.CH4_LD_button = tk.Button(self.LD_SelectFrame, text='CH4', fg='black', bd=3, relief='raised',
                                       command=lambda:  self.ld_toggle(self.ld_ch4))
        self.CH4_LD_button.grid(row=x+1, column=y+2, padx=0, pady=10)




        self.schedule_button = tk.Button(self.LD_SelectFrame, text="Run Scheduler", height=1,fg='Azure', background='#303030', command=lambda:  self.controller.scheduler())
        self.schedule_button.grid(row=x+2,column=y,padx=20,pady=0,columnspan=3,sticky="news")


        self.schedule_button = tk.Button(self.LD_SelectFrame, text="Auto Measure in position", height=1,fg='Azure', background='#303030',command=lambda:  self.controller.auto_measurement())
        self.schedule_button.grid(row=x+3,column=y,padx=20,pady=0,columnspan=3,sticky="news")



    def DataInterface(self,x,y):
        self.DataFrame = tk.Frame(self,relief="ridge",bd=2,bg="gray")
        self.DataFrame.grid(row=x,column=y,sticky='news')

        self.Collect_Data = tk.Button(self.DataFrame, text='COLLECT DATA', fg='black',bd=3,relief='raised', command=lambda: self.ld.collect_data(self.ard))
        self.Collect_Data.grid(row=x, column=y, sticky='nesw', padx=0, pady=0)

        self.Clear_Data = tk.Button(self.DataFrame, text='Clear Data', fg='black',bd=3,relief='raised', command=lambda: self.ard.clear_Data())
        self.Clear_Data.grid(row=x, column=y+1, sticky='nesw', padx=0, pady=0)

        #self.Save_Data = tk.Button(self.DataFrame, text='Save Data', fg='black',bd=3,relief='raised', command=lambda: self.ard.save_Data(self.ld.name))
        self.Save_Data = tk.Button(self.DataFrame, text='Save Data', fg='black',bd=3,relief='raised', command=lambda: self.ld.save_data() )
        self.Save_Data.grid(row=x, column=y+2, sticky='nesw', padx=0, pady=0)
            
        self.Plot_button = tk.Button(self.DataFrame, text="Plot", bd=3, relief='raised',width=15,command=lambda: Graph.plot_data(self.ld.latestdatafile))
        self.Plot_button.grid(row=x+1,column=y, sticky='nesw', padx=0, pady=0)

        self.Quit_plot_button = tk.Button(self.DataFrame, text="Terminate Data Acq",command=lambda: self.ard.terminate())
        self.Quit_plot_button.grid(row=x+1,column=y+2,sticky='e')

    def RampInterface(self,x,y):
        self.RampFrame= tk.Frame(self,relief="ridge",bd=2,bg="gray")
        self.RampFrame.grid(row=x,column=y,sticky='news')

        self.Label1 = tk.Label(self.RampFrame, text="A min", fg='Azure', background='#303030')
        self.Label1.grid(row=x, column=y, sticky='we')

        self.Label2 = tk.Label(self.RampFrame, text="(10x mA)  A max ", height=1, fg='Azure', background='#303030')
        self.Label2.grid(row=x, column=y+1, sticky='ew')

        self.Label3 = tk.Label(self.RampFrame, text="T(secs)", width=10, height=1, fg='Azure', background='#303030')
        self.Label3.grid(row=x, column=y+2, sticky='ww',padx=5)

        self.V1_set_field = tk.Entry(self.RampFrame, width=6)
        self.V1_set_field.grid(row=x+1, column=y, padx=0, pady=0, sticky='w')
        
        self.V2_set_field = tk.Entry(self.RampFrame, width=6)
        self.V2_set_field.grid(row=x+1, column=y+1, padx=0, pady=0, sticky='w')

        self.T_set_field = tk.Entry(self.RampFrame, width=6)
        self.T_set_field.grid(row=x+1, column=y+2, padx=20, pady=0, sticky='w')

        #self.Ramp_Start_button = tk.Button(self.RampFrame, text='Start Ramp', fg='black', bd=3, relief='raised', command=lambda: self.ld.start_Ramp(self.ard))
        #self.Ramp_Start_button.grid(row=x+2, column=y, padx=0, pady=0, sticky='we')

        self.Ramp_Update_button = tk.Button(self.RampFrame, text='Update Ramp', fg='black', bd=3, relief='raised', command=lambda: self.ld.update_Ramp(int(self.V1_set_field.get()),int(self.V2_set_field.get()),int(self.T_set_field.get())))
        self.Ramp_Update_button.grid(row=x+2, column=y+1, padx=0, pady=0, sticky='we')

        self.Ramp_Stop_button = tk.Button(self.RampFrame, text='Stop Ramp', fg='black', bd=3, relief='raised',command=lambda: self.ld.terminate_Ramp())
        self.Ramp_Stop_button.grid(row=x+2, column=y+2, padx=0, pady=0, sticky='we')

    def Machine_States(self,x,y):
        self.MachStateFrame = tk.Frame(self,relief="ridge",bd=2,bg="gray")
        self.MachStateFrame.grid(row=x,column=y,sticky='news')

        self.Machine_door_reply = tk.StringVar()
        self.Machine_door_reply.set("---")

        self.Machine_position_reply = tk.StringVar()
        self.Machine_position_reply.set("---")

        self.Machine_temperature_reply = tk.StringVar()
        self.Machine_temperature_reply.set("---")


        self.Machine_fan_reply = tk.StringVar()
        self.Machine_fan_reply.set("---")
        
        self.LIA_reply = tk.StringVar()
        self.LIA_reply.set("---")


        """Machine State"""

        self.Machine_Label = tk.Label(self.MachStateFrame, text="Machine State")
        self.Machine_Label.grid(row=x, column=y,columnspan=3, sticky='news')

        self.Door_State_label = tk.Label(self.MachStateFrame, text = "Door State  :",fg ='Azure', background='#303030')
        self.Door_State_label.grid(row=x+1,column=y,sticky='w')

        self.Fan_State_label = tk.Label(self.MachStateFrame, text = "Fan State  :", fg = 'Azure', background='#303030')
        self.Fan_State_label.grid(row=x+2,column=y,sticky='w')

        self.Position_label = tk.Label(self.MachStateFrame, text = "Position  :", fg = 'Azure', background='#303030')
        self.Position_label.grid(row=x+3,column=y,sticky='w')

        self.Temperature_label = tk.Label(self.MachStateFrame, text = "Temp  :", fg = 'Azure', background='#303030')
        self.Temperature_label.grid(row=x+4,column=y,sticky='w')

        self.LD1_label = tk.Label(self.MachStateFrame, text = "LD1 State  :", fg = 'Azure', background='#303030')
        self.LD1_label.grid(row=x+5,column=y,sticky='w')

        self.LD2_label = tk.Label(self.MachStateFrame, text = "LD2 State  :", fg = 'Azure', background='#303030')
        self.LD2_label.grid(row=x+6,column=y,sticky='w')

        self.LD3_label = tk.Label(self.MachStateFrame, text = "LD3 State  :", fg = 'Azure', background='#303030')
        self.LD3_label.grid(row=x+7,column=y,sticky='w')

        self.Components_label = tk.Label(self.MachStateFrame, text = "Components State  :", fg = 'Azure', background='#303030')
        self.Components_label.grid(row=x+8,column=y,sticky='w')

        self.PSU_label = tk.Label(self.MachStateFrame, text = "PSU State  :", fg = 'Azure', background='#303030')
        self.PSU_label.grid(row=x+9,column=y,sticky='w')
        
        self.LIA_sensitivity_label = tk.Label(self.MachStateFrame, text="LIA value :", fg='Azure', background='#303030')
        self.LIA_sensitivity_label.grid(row=x+10, column=y, sticky='w')


        


        """Entry Machine"""

        self.Door_Label_txt = tk.Entry(self.MachStateFrame, textvariable=self.Machine_door_reply, fg='Azure', background='#303030')
        self.Door_Label_txt.grid(row=x+1, column=y+1)

        self.Position_Label_txt = tk.Entry(self.MachStateFrame, textvariable=self.Machine_position_reply, fg='Azure', background='#303030')
        self.Position_Label_txt.grid(row=x+3, column=y+1, sticky='e')

        self.Temperature_Label_txt = tk.Entry(self.MachStateFrame, textvariable=self.Machine_temperature_reply, fg='Azure', background='#303030')
        self.Temperature_Label_txt.grid(row=x+4, column=y+1, sticky='e')
        
        self.LIA_sensitivity_label = tk.Entry(self.MachStateFrame, textvariable=self.LIA_reply, fg='Azure',width=5, background='#303030')
        self.LIA_sensitivity_label.grid(row=x+10, column=y+1, sticky='e')
        
      
               


        """Canvas Machine"""


        self.Fan_Canvas = tk.Canvas(self.MachStateFrame, width=10, height=10, bg='White')
        self.Fan_Canvas.grid(row=x+2,column=y+1,sticky='e')


        self.LD1_Canvas = tk.Canvas(self.MachStateFrame, width=10, height=10, bg='White')
        self.LD1_Canvas.grid(row=x+5,column=y+1,sticky='e')

        self.LD2_Canvas = tk.Canvas(self.MachStateFrame, width=10, height=10, bg='White')
        self.LD2_Canvas.grid(row=x+6,column=y+1,sticky='e')

        self.LD3_Canvas = tk.Canvas(self.MachStateFrame, width=10, height=10, bg='White')
        self.LD3_Canvas.grid(row=x+7,column=y+1,sticky='e')

        self.Components_Canvas = tk.Canvas(self.MachStateFrame, width=10, height=10, bg='White')
        self.Components_Canvas.grid(row=x+8,column=y+1,sticky='e')

        self.PSU_Canvas = tk.Canvas(self.MachStateFrame, width=10, height=10, bg='White')
        self.PSU_Canvas.grid(row=x+9,column=y+1,sticky='e')

    def LD_States(self,x,y):
        self.InfoFrame = tk.Frame(self,relief="ridge",bd=2,bg="gray")
        self.InfoFrame.grid(row=x,column=y,rowspan=2,sticky='news')
        self.InfoFrame.rowconfigure(0, weight=1)

        self.LD_name = tk.StringVar()
        self.LD_name.set("State of Driver")
        
        self.Current_Set_reply = tk.StringVar()
        self.Current_Set_reply.set("---")

        self.LD_Enable_reply = tk.StringVar()
        self.LD_Enable_reply.set("---")

        self.Temp_set_reply = tk.StringVar()
        self.Temp_set_reply.set("---")

        self.TEC_Enable_reply = tk.StringVar()
        self.TEC_Enable_reply.set("---")

        self.Error_reply = tk.StringVar()

        self.temp_reply = tk.StringVar()
        self.temp_reply.set("---")    #LDriver.LD_Obj.temp_field

        self.current_reply = tk.StringVar()
        self.current_reply.set("---")
        
        self.RampMin_reply = tk.StringVar()
        self.RampMin_reply.set("---")

        self.RampMax_reply = tk.StringVar()
        self.RampMax_reply.set("---")

        self.RampTime_reply = tk.StringVar()
        self.RampTime_reply.set("---")

        self.duration_reply = tk.StringVar()
        self.duration_reply.set("---")

        self.default_current_reply = tk.StringVar()
        self.default_current_reply.set("---")

        self.max_current_limit_reply = tk.StringVar()
        self.max_current_limit_reply.set("---")

        self.max_tec_current_limit_reply = tk.StringVar()
        self.max_tec_current_limit_reply.set("---")

        




        """Driver State"""

        self.Driver_label = tk.Label(self.InfoFrame, textvariable=self.LD_name)
        self.Driver_label.grid(row=x+1,column=y,columnspan=2,sticky='wen')

        self.Start_Stop_label = tk.Label(self.InfoFrame, text = "Start/Stop  :",fg='Azure', background='#303030')
        self.Start_Stop_label.grid(row=x+2,column=y,sticky='w')

        self.Current_Set_label = tk.Label(self.InfoFrame, text="Current Set  :",fg='Azure', background='#303030')
        self.Current_Set_label.grid(row=x+3, column=y, sticky='w')

        self.Enable_label = tk.Label(self.InfoFrame, text="Enable  :",fg='Azure', background='#303030')
        self.Enable_label.grid(row=x+4, column=y, sticky='w')

        self.LD_Ext_Int_label = tk.Label(self.InfoFrame, text="Ext NTC Interlock  :",fg='Azure', background='#303030')
        self.LD_Ext_Int_label.grid(row=x+5, column=y, sticky='w')

        self.LD_Interlock_label = tk.Label(self.InfoFrame, text="Interlock  :",fg='Azure', background='#303030')
        self.LD_Interlock_label.grid(row=x+6, column=y, sticky='w')

        """State of the TEC Labels"""

        self.Tec_State_label = tk.Label(self.InfoFrame, text="State of the TEC")
        self.Tec_State_label.grid(row=x+7, column=y,columnspan=2, sticky='wen')

        self.ON_OFF_label = tk.Label(self.InfoFrame, text="ON/OFF  :",fg='Azure', background='#303030')
        self.ON_OFF_label.grid(row=x+8, column=y, sticky='w')

        self.Temperature_Set_label = tk.Label(self.InfoFrame, text="Temperature Set  :",fg='Azure', background='#303030')
        self.Temperature_Set_label.grid(row=x+9, column=y, sticky='w')

        self.Enable_label = tk.Label(self.InfoFrame, text="Temp Enable  :",fg='Azure', background='#303030')
        self.Enable_label.grid(row=x+10, column=y, sticky='w')

        # Canvas-Entry State of the Driver

        self.Start_Stop_Canvas = tk.Canvas(self.InfoFrame,width=10,height=10,bg='White')
        self.Start_Stop_Canvas.grid(row=x+2,column=y+1,sticky='e')

        self.Current_Set_txt = tk.Label(self.InfoFrame, textvariable=self.Current_Set_reply,fg='Azure', background='#303030')
        self.Current_Set_txt.grid(row=x+3,column=y+1,sticky='e')

        self.LD_Enable_txt = tk.Label(self.InfoFrame,textvariable=self.LD_Enable_reply,fg='Azure', background='#303030')
        self.LD_Enable_txt.grid(row=x+4,column=y+1,sticky='e')

        self.LD_Ext_NTC_Canvas = tk.Canvas(self.InfoFrame, width=10, height=10, bg='White')
        self.LD_Ext_NTC_Canvas.grid(row=x+5,column=y+1,sticky='e')

        self.LD_Interlock_Canvas = tk.Canvas(self.InfoFrame, width=10, height=10, bg='White')
        self.LD_Interlock_Canvas.grid(row=x+6,column=y+1,sticky='e')

        ## Canvas-Entry State of the TEC

        self.TEC_ON_OFF_Canvas = tk.Canvas(self.InfoFrame, width=10, height=10, bg='white')
        self.TEC_ON_OFF_Canvas.grid(row=x+8,column=y+1,sticky='e')

        self.Temperature_txt = tk.Label(self.InfoFrame,textvariable=self.Temp_set_reply,fg='Azure', background='#303030')
        self.Temperature_txt.grid(row=x+9,column=y+1,sticky='e')

        self.TEC_Enable_txt = tk.Label(self.InfoFrame,textvariable=self.TEC_Enable_reply,fg='Azure', background='#303030')
        self.TEC_Enable_txt.grid(row=x+10,column=y+1,sticky='e')


        ### Lock State Labels

        self.Status_label = tk.Label(self.InfoFrame, text="Lock Status")
        self.Status_label.grid(row=x+11, column=y,columnspan=2, sticky='NESW')

        self.LOCK_Interlock_label = tk.Label(self.InfoFrame, text="Interlock   :", fg='Azure', background='#303030')
        self.LOCK_Interlock_label.grid(row=x+12, column=y, sticky='w')

        self.LD_overcurrent_label = tk.Label(self.InfoFrame, text="LD over current   :", fg='Azure', background='#303030')
        self.LD_overcurrent_label.grid(row=x+13, column=y, sticky='w')

        self.LD_overheat_label = tk.Label(self.InfoFrame, text="LD overheat   :", fg='Azure', background='#303030')
        self.LD_overheat_label.grid(row=x+14, column=y, sticky='w')

        self.LOCK_Ext_NTC_label = tk.Label(self.InfoFrame, text="External NTC Interlock   :", fg='Azure', background='#303030')
        self.LOCK_Ext_NTC_label.grid(row=x+15, column=y, sticky='w')

        self.Tec_error_label = tk.Label(self.InfoFrame, text="TEC error   :",fg='Azure', background='#303030')
        self.Tec_error_label.grid(row=x+16, column=y, sticky='w')

        self.Tec_self_heat_label = tk.Label(self.InfoFrame, text="TEC self-heat   :", fg='Azure', background='#303030')
        self.Tec_self_heat_label.grid(row=x+17, column=y, sticky='w')

        ##Canvas-Entry LOCK


        self.LOCK_Interlock_Canvas = tk.Canvas(self.InfoFrame,width=10,height=10,bg='White')
        self.LOCK_Interlock_Canvas.grid(row=x+12,column=y+1,sticky='e')

        self.LOCK_LD_overcurrent = tk.Canvas(self.InfoFrame,width=10,height=10,bg='White')
        self.LOCK_LD_overcurrent.grid(row=x+13,column=y+1,sticky='e')

        self.LOCK_LD_overheat = tk.Canvas(self.InfoFrame,width=10,height=10,bg='White')
        self.LOCK_LD_overheat.grid(row=x+14,column=y+1,sticky='e')

        self.LOCK_Ext_NTC_Interlock = tk.Canvas(self.InfoFrame,width=10,height=10,bg='White')
        self.LOCK_Ext_NTC_Interlock.grid(row=x+15,column=y+1,sticky='e')

        self.LOCK_TEC_error = tk.Canvas(self.InfoFrame,width=10,height=10,bg='White')
        self.LOCK_TEC_error.grid(row=x+16,column=y+1,sticky='e')

        self.LOCK_Self_heat = tk.Canvas(self.InfoFrame,width=10,height=10,bg='White')
        self.LOCK_Self_heat.grid(row=x+17,column=y+1,sticky='e')

        ## Errors

        self.Status_label = tk.Label(self.InfoFrame, text="ERRORS", height=1,fg='red',bg='white')
        self.Status_label.grid(row=x+18, column=y,columnspan=2, sticky='wen')

        #self.grid_rowconfigure(, minsize=10)

        self.Error_txt = tk.Entry(self.InfoFrame,textvariable=self.Error_reply)
        self.Error_txt.grid(row=x+19,column=y,columnspan=2,sticky='wen')

        self.Temp_label = tk.Label(self.InfoFrame, text="Real Temp (°C)  :", fg='Azure', background='#303030')
        self.Temp_label.grid(row=x+20, column=y, sticky='w')

        self.Temp_label = tk.Label(self.InfoFrame, textvariable=self.temp_reply, fg='Azure', background='#303030')
        self.Temp_label.grid(row=x+20, column=y+1, sticky='e')

        self.current_label = tk.Label(self.InfoFrame, text="Real Current (mA)  :", fg='Azure', background='#303030')
        self.current_label.grid(row=x+21, column=y, sticky='w')

        self.current_label = tk.Label(self.InfoFrame, textvariable=self.current_reply, fg='Azure', background='#303030')
        self.current_label.grid(row=x+21, column=y+1, sticky='e')
        
        self.Ramp_Min_Label = tk.Label(self.InfoFrame, text="Ramp Min (10x mA) :", fg='Azure', background='#303030')
        self.Ramp_Min_Label.grid(row=x+22, column=y, sticky='w')

        self.Ramp_Min_Label = tk.Label(self.InfoFrame, textvariable=self.RampMin_reply, fg='Azure', background='#303030')
        self.Ramp_Min_Label.grid(row=x+22, column=y+1, sticky='e')

        self.Ramp_Max_Label = tk.Label(self.InfoFrame, text="Ramp Max (10x mA) :", fg='Azure', background='#303030')
        self.Ramp_Max_Label.grid(row=x+23, column=y, sticky='w')

        self.Ramp_Max_Label = tk.Label(self.InfoFrame, textvariable=self.RampMax_reply, fg='Azure', background='#303030')
        self.Ramp_Max_Label.grid(row=x+23, column=y+1, sticky='e')

        self.Ramp_Time_label = tk.Label(self.InfoFrame, text="Time (sec) :", fg='Azure', background='#303030')
        self.Ramp_Time_label.grid(row=x+24, column=y, sticky='w')

        self.Ramp_Time_label = tk.Label(self.InfoFrame, textvariable=self.RampTime_reply, fg='Azure', background='#303030')
        self.Ramp_Time_label.grid(row=x+24, column=y+1, sticky='e')

        self.duration_label = tk.Label(self.InfoFrame, text="Duration (sec) :", fg='Azure', background='#303030')
        self.duration_label.grid(row=x+25, column=y, sticky='w')

        self.duration_label = tk.Label(self.InfoFrame, textvariable=self.duration_reply, fg='Azure', background='#303030')
        self.duration_label.grid(row=x+25, column=y+1, sticky='e')

        self.default_current_label = tk.Label(self.InfoFrame, text="Default Current (mA) :", fg='Azure', background='#303030')
        self.default_current_label.grid(row=x+26, column=y, sticky='w')

        self.default_current_label = tk.Label(self.InfoFrame, textvariable=self.duration_reply, fg='Azure', background='#303030')
        self.default_current_label.grid(row=x+26, column=y+1, sticky='e')

        self.max_current_label = tk.Label(self.InfoFrame, text="Max Current (mA) :", fg='Azure', background='#303030')
        self.max_current_label.grid(row=x+27, column=y, sticky='w')

        self.max_current_label = tk.Label(self.InfoFrame, textvariable=self.max_current_limit_reply, fg='Azure', background='#303030')
        self.max_current_label.grid(row=x+27, column=y+1, sticky='e')

        self.max_tec_reply_label = tk.Label(self.InfoFrame, text="Tec Max Limit (A) :", fg='Azure', background='#303030')
        self.max_tec_reply_label.grid(row=x+28, column=y, sticky='w')

        self.max_tec_reply_label = tk.Label(self.InfoFrame, textvariable=self.max_tec_current_limit_reply, fg='Azure', background='#303030')
        self.max_tec_reply_label.grid(row=x+28, column=y+1, sticky='e')
        

        
        

    def parse_reply(self,laser_object):

        laser_object.refresh_status()

        self.LD_name.set(laser_object.name + ' - Laser Driver State')

        rep=laser_object.Error_reply
        if rep == 'K0000 0000':
            self.Error_reply.set("Request or set the parameter that does not exist")
        else:
            self.Error_reply.set(laser_object.Error_reply)


        self.temp_reply.set(laser_object.Temperature)
        self.current_reply.set(laser_object.LD_current)
        self.RampMin_reply.set(laser_object.RampMin)
        self.RampMax_reply.set(laser_object.RampMax)
        self.RampTime_reply.set(laser_object.RampTime)
        self.duration_reply.set(laser_object.measurement_duration)
        self.default_current_reply.set(laser_object.default_current)
        self.max_current_limit_reply.set(laser_object.max_current_limit)
        self.max_tec_current_limit_reply.set(laser_object.max_tec_current_limit)

        

        #d.LD_State:
        self.Current_Set_reply.set(laser_object.Current_Set)
        self.LD_Enable_reply.set(laser_object.LD_Enable)       
           
        if laser_object.LD_state == False:
            rectangleId = self.Start_Stop_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
        else:
            rectangleId = self.Start_Stop_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')


        if laser_object.Ext_NTC_interlock == 'Allowed':
            rectangleId = self.LD_Ext_NTC_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')
            #print("External NTC Interlock: Allowed")
        else:
            rectangleId = self.LD_Ext_NTC_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
            #print("External NTC Interlock:Denied")

        if laser_object.Interlock == 'Allowed':
            rectangleId = self.LD_Interlock_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')
            #print("Interlock: Allowed")
        else:
            rectangleId = self.LD_Interlock_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
            #print("Interlock: Denied")


        #d.Lock_Status:
        if laser_object.Lock_Interlock == True:
            rectangleId = self.LOCK_Interlock_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
            #print("Interlock Allowed")
        else:
            rectangleId = self.LOCK_Interlock_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')
            #print("Interlock Denied")

        if laser_object.Lock_OverCurrent == True:
            rectangleId = self.LOCK_LD_overcurrent.create_oval(2, 2, 10, 10, width=0, fill='red')
            #print("LD overcurrent ON")
        else:
            rectangleId = self.LOCK_LD_overcurrent.create_oval(2, 2, 10, 10, width=0, fill='green')
            #print("LD overcurrent OFF")

        if laser_object.Lock_OverHeat == True:
            rectangleId = self.LOCK_LD_overheat.create_oval(2, 2, 10, 10, width=0, fill='red')
            #print("LD Overheat ON")
        else:
            rectangleId = self.LOCK_LD_overheat.create_oval(2, 2, 10, 10, width=0, fill='green')
            #print("LD Overheat OFF")

        if laser_object.Lock_ExtNTCInterlock == True:
            rectangleId = self.LOCK_Ext_NTC_Interlock.create_oval(2, 2, 10, 10, width=0, fill='red')
            #print("External NTC Interlock Allowed")
        else:
            rectangleId = self.LOCK_Ext_NTC_Interlock.create_oval(2, 2, 10, 10, width=0, fill='green')
            #print("External NTC Interlock Denied")

        if laser_object.Lock_TECError == True:
            rectangleId = self.LOCK_TEC_error.create_oval(2, 2, 10, 10, width=0, fill='red')
            #print("TEC Error TRUE")
        else:
            rectangleId = self.LOCK_TEC_error.create_oval(2, 2, 10, 10, width=0, fill='green')
            #print("TEC Error FALSE")

        if laser_object.Lock_TEC_selfHeat == True:
            rectangleId = self.LOCK_Self_heat.create_oval(2, 2, 10, 10, width=0, fill='red')
            #print("TEC Self_heat ON")
        else:
            rectangleId = self.LOCK_Self_heat.create_oval(2, 2, 10, 10, width=0, fill='green')
            #print("TEC Self_heat OFF")

        #d.TEC_State:
            
        if laser_object.TEC_state == False:
            rectangleId = self.TEC_ON_OFF_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
        else:
            rectangleId = self.TEC_ON_OFF_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')

        self.Temp_set_reply.set( laser_object.Temp_set)
        self.TEC_Enable_reply.set(laser_object.TEC_Enable)

    def machine_update(self,machine_object):
        machine_object.get_status()

        self.Machine_door_reply.set(machine_object.doorstate)
        self.Machine_position_reply.set(machine_object.position)
        self.Machine_temperature_reply.set(machine_object.temperature)
        self.LIA_reply.set(machine_object.lia_val)
        


        if machine_object.fanstate == '0\r\n':
            rectangleId = self.Fan_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
        elif machine_object.fanstate == '1\r\n': 
            rectangleId = self.Fan_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')

        if machine_object.LD1State == '0\r\n':
            rectangleId = self.LD1_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
        elif machine_object.LD1State == '1\r\n':
            rectangleId = self.LD1_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')

        if machine_object.LD2State == '0\r\n':
            rectangleId = self.LD2_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
        elif machine_object.LD2State == '1\r\n':
            rectangleId = self.LD2_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')

        if machine_object.LD3State == '0\r\n':
            rectangleId = self.LD3_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
        elif machine_object.LD3State == '1\r\n':
            rectangleId = self.LD3_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')

        if machine_object.ComponentsState == '0\r\n':
            rectangleId = self.Components_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
        elif machine_object.ComponentsState == '1\r\n':
            rectangleId = self.Components_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')



        if machine_object.PSUState == '0\r\n':
            rectangleId = self.PSU_Canvas.create_oval(2, 2, 10, 10, width=0, fill='red')
        elif machine_object.PSUState == '1\r\n':
            rectangleId = self.PSU_Canvas.create_oval(2, 2, 10, 10, width=0, fill='green')



if __name__ == '__main__':
    my_window = MainWin()
    my_window.mainloop()