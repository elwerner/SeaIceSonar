# -*- coding: utf-8 -*-
'''
#######################################
Operating Echosounders Icelab

@author: Ellen Werner 
ellen.werner@hcu-hamburg.de
date: 27.07.2022
Triggered Datalogging of Airmar, Ping & Tritec sonar
#######################################
'''

### imports
import serial
import time
import datetime
import numpy as np
from brping import Ping1D

### main loop over all three sensors 
try:
    ###### Initializing Sensors ######
    
    ## Airmar 
    myAirmarOut = serial.Serial(
    port='COM6',\
    baudrate=4800,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=1)

    myAirmarIn = serial.Serial(
    port='COM19',\
    baudrate=4800,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=1)
    
    print("------------------------------------")
    print("Airmar connected at: " + myAirmarOut.name + " and " + myAirmarIn.name)
    print("starting Airmar...")
    
    ## Tritech
    myTritech = serial.Serial(
    port='COM46',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

    print("------------------------------------")
    print("Tritech connected at: " + myTritech.name)
    print("starting Tritech...")

    ## Ping
    myPing = Ping1D()
    
    print("------------------------------------")
    myPing.connect_serial('COM29', 115200)
    print("starting Ping...")
    
    
    
    
    ###### Set instrument configuration #######
    
    ## Airmar 
    myAirmarIn.write('$PAMTC,OPTION,SET,PING,ON\r\n'.encode('ascii'))           # start Pinging
    time.sleep(3) 
    myAirmarIn.write('$PAMTC,OPTION,SET,OUTPUTMC\r\n'.encode('ascii'))          # Change nmea output settings to: NMEA depth output after each ping 
    myAirmarIn.write('$PAMTC,OPTION,SET,PING,OFF\r\n'.encode('ascii'))          # stop Pinging
    myAirmarIn.write('$PAMTC,EN,MTW,0\r\n'.encode('ascii'))                     # Stop output of MTW data (so only DPT data is output)
    myAirmarIn.write('$PAMTC,OPTION,SET,SOSTW,15000\r\n'.encode('ascii'))       # Set speed of sound to 1500 m/s
    myAirmarOut.flushInput()
    
    ## Tritec
    myTritech.write(b'Z')                                           # Change the mode from free running to interrogate mode
    
    ## Ping
    myPing.set_speed_of_sound(1500000)                              # Set the speed of sound to 1500 m/s (1500000 mm/s) 
    myPing.set_mode_auto(0)                                                     # Set auto_mode off
    myPing.set_gain_setting(3)                                                  # Set Gain manually to 12.9
    myPing.set_range(0,1000)                                                     # Set range to 500 mm
    myPing.set_ping_enable(0)                                                   # Stop Pinging
    
    
    ###### Reading the data from sensor ######

     
    starttime=time.time()
    while True:
        
        ### AIRMAR ### 
        try:
            myAirmarIn.write('$PAMTC,OPTION,SET,PING,ON\r\n'.encode('ascii'))       # start Pinging for 1sec
            myAirmarOut.flushInput()
            time.sleep(1)                                                                               
            
            nmea = myAirmarOut.readline()                                           # read out nmea data 
            nmea = nmea.strip().decode('ascii', errors='replace')
            timestamp = str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))  # create timestamp
            print(f'{timestamp},{nmea}')                                            # print to terminal
            myAirmarIn.write('$PAMTC,OPTION,SET,PING,OFF\r\n'.encode('ascii'))      # stop Pinging
            
            ## Save measurements in a csv-file
            with open(f'DataLogs/GroßerTank_Versuch4/AirmarLog_{timestamp[0:10]}.csv', 'a') as f:       ### <- EDIT FILENAME HERE
                f.write(f'{timestamp},{nmea}\n')
            #shutil.copyfile(f'DataLogs/AirmarLog_{timestamp[0:10]}.csv',f'C:/Users/labuser/Desktop/Copytoftp/AirmarLog_{timestamp[0:10]}.csv')
            
            time.sleep(2.0 - ((time.time() - starttime) % 2.0))                     ### <- set the timeinterval 
        except Exception: 
            pass
              
        ### TRITECH ###
        try:
            time.sleep(1)
            myTritech.write(b'Z')                                                   # trigger one ping
            
            data = myTritech.readline()                                             # read out data 
            data = data.strip().decode()
            timestamp = str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))  # create timestamp
            print(f'{timestamp},{data}')                                            # print to terminal
            
            ## Save measurements in a csv-file
            with open(f'DataLogs/GroßerTank_Versuch4/TritechLog_{timestamp[0:10]}.csv', 'a') as f:      ### <- EDIT FILENAME HERE
                f.write(f'{timestamp},{data}\n')
            #shutil.copyfile(f'DataLogs/TritechLog_{timestamp[0:10]}.csv',f'C:/Users/labuser/Desktop/Copytoftp/Tritech_{timestamp[0:10]}.csv')
            
            time.sleep(2.0 - ((time.time() - starttime) % 2.0))                     ### <- set the timeinterval 
        except Exception: 
            pass
        
        ### PING ###
        try:
            myPing.set_ping_enable(1)                                               # Start Pinging
            time.sleep(1)      
            
            newdata = myPing.get_distance_simple()                                  # read out data
            newprofile = myPing.get_profile()
            proc_temp = myPing.get_processor_temperature()
            pcb_temp = myPing.get_pcb_temperature()
            general_info = myPing.get_general_info()
            
            timestamp = str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))  # create timestamp
            print(f'{timestamp},{newdata["distance"]/1000},{newdata["confidence"]}')   # print to terminal
            profile = np.frombuffer(newprofile["profile_data"], np.uint8).tolist()

        
            myPing.set_ping_enable(0)
        
            ## Save measurements in a csv-file
            with open(f'DataLogs/GroßerTank_Versuch4/PingLog_{timestamp[0:10]}.csv', 'a') as f:    ### <- EDIT FILENAME HERE
                f.write(f'{timestamp},{newdata["distance"]/1000},{newdata["confidence"]}\n')
            with open(f'DataLogs/GroßerTank_Versuch4/PingProfileLog_{timestamp[0:10]}.csv', 'a') as f:    ### <- EDIT FILENAME HERE
                f.write(f'{timestamp},{newprofile["distance"]/1000},{newprofile["confidence"]},{newprofile["transmit_duration"]},{newprofile["ping_number"]},{newprofile["scan_start"]},{newprofile["scan_length"]},{newprofile["gain_setting"]},{",".join(map(str, profile))}\n')
            with open(f'DataLogs/GroßerTank_Versuch4/PingTempLog_{timestamp[0:10]}_test.csv', 'a') as f:    ### <- EDIT FILENAME HERE
                f.write(f'{timestamp},{general_info["voltage_5"]/1000},{proc_temp["processor_temperature"]/100},{pcb_temp["pcb_temperature"]/100}\n')
            #shutil.copyfile(f'DataLogs/PingLog_{timestamp[0:10]}.csv',f'C:/Users/labuser/Desktop/Copytoftp/PingLog_{timestamp[0:10]}.csv')
            #shutil.copyfile(f'DataLogs/PingProfileLog_{timestamp[0:10]}.csv',f'C:/Users/labuser/Desktop/Copytoftp/PingProfileLog_{timestamp[0:10]}.csv')
            
     
            time.sleep(2.0 - ((time.time() - starttime) % 2.0))                     ### <- set the timeinterval 
        except Exception: 
            pass
    
    myAirmarIn.close()
    myAirmarOut.close()  
    myTritech.close()
               

except serial.SerialException as err:
    print("Serial Port Error: \n" + str(err))
    try:
        myAirmarIn.close()
    except:
        pass
    try:
        myAirmarOut.close()
    except: 
        pass
    try:
        myTritech.close()
    except:
        pass
    quit()

except KeyboardInterrupt:
    print("Keyboard break")
    try:
        myAirmarIn.close()
    except:
        pass
    try:
        myAirmarOut.close()
    except: 
        pass
    try:
        myTritech.close()
    except:
        pass
    
    
except Exception as err:
    print(err)
    try:
        myAirmarIn.close()
    except:
        pass
    try:
        myAirmarOut.close()
    except: 
        pass
    try:
        myTritech.close()
    except:
        pass
    quit()

