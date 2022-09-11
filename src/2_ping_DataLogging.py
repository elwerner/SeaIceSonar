# -*- coding: utf-8 -*-
'''
#######################################
Operating Echosounders Icelab

@author: Ellen Werner 
ellen.werner@hcu-hamburg.de
date: 19.07.2022
Data Logging with Ping sonar
#######################################
'''

### imports
from brping import Ping1D
import time
import datetime
import sys
import numpy as np

### Initializing Ping via serial connection
try:
    
    myPing = Ping1D()
    myPing.connect_serial('COM29', 115200)
    
    if myPing.initialize() is False:
        print("Failed to initialize Ping!")
        exit(1)
    
    print("------------------------------------")
    print("starting Ping..")
    
    
    ### Set measurement parameters on the sensor 
    
    myPing.set_speed_of_sound(1426000)                                          # Set the speed of sound to 1500 m/s (1500000 mm/s) 
    myPing.set_mode_auto(0)                                                     # Set auto_mode off
    myPing.set_gain_setting(3)                                                  # Set Gain manually to 12.9
    myPing.set_range(0,500)                                                     # Set range to 500 mm
    
    myPing.set_ping_enable(0)                                                    # Stop Pinging
    
    ### Reading the data from sensor 
    
    ## Read and print distance measurements with confidence 
    starttime=time.time()
    while True:
        myPing.set_ping_enable(1)                                               # Start Pinging
        time.sleep(1)      
        
        newdata = myPing.get_distance_simple()                                  # read out data
        newprofile = myPing.get_profile()
        proc_temp = myPing.get_processor_temperature()
        pcb_temp = myPing.get_pcb_temperature()
        general_info = myPing.get_general_info()
        
        timestamp = str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))  # create timestamp
        print(f'{timestamp},{newdata["distance"]/1000},{newdata["confidence"]}')   # print to terminal
        # print(f'{timestamp},{newprofile["distance"]/1000},{newprofile["confidence"]},{newprofile["transmit_duration"]},{newprofile["ping_number"]},{newprofile["scan_start"]},{newprofile["scan_length"]},{newprofile["gain_setting"]},{np.frombuffer(newprofile["profile_data"], np.uint8)}')
        profile = np.frombuffer(newprofile["profile_data"], np.uint8).tolist()
        #print(",".join(map(str, profile)))
        print(f'{timestamp},{general_info["voltage_5"]/1000},{general_info["ping_interval"]},{general_info["mode_auto"]}')
        print(f'{timestamp},{proc_temp["processor_temperature"]/100},{pcb_temp["pcb_temperature"]/100}')
        
        myPing.set_ping_enable(0)                                               # Stop Pinging
    
        ## Save measurements in a csv-file
        with open(f'DataLogs/PingLogTest_{timestamp[0:10]}_test.csv', 'a') as f:    ### <- EDIT FILENAME HERE
            f.write(f'{timestamp},{newdata["distance"]/1000},{newdata["confidence"]}\n')
        # with open(f'DataLogs/PingProfileLog_{timestamp[0:10]}.csv', 'a') as f:    ### <- EDIT FILENAME HERE
            # f.write(f'{timestamp},{newprofile["distance"]/1000},{newprofile["confidence"]},{newprofile["transmit_duration"]},{newprofile["ping_number"]},{newprofile["scan_start"]},{newprofile["scan_length"]},{newprofile["gain_setting"]},{profile}\n')
        with open(f'DataLogs/PingProfileLogTest_{timestamp[0:10]}.csv', 'a') as f:    ### <- EDIT FILENAME HERE
            f.write(f'{timestamp},{newprofile["distance"]/1000},{newprofile["confidence"]},{newprofile["transmit_duration"]},{newprofile["ping_number"]},{newprofile["scan_start"]},{newprofile["scan_length"]},{newprofile["gain_setting"]},{",".join(map(str, profile))}\n')
        with open(f'DataLogs/PingTempTest_{timestamp[0:10]}_test.csv', 'a') as f:    ### <- EDIT FILENAME HERE
            f.write(f'{timestamp},{general_info["voltage_5"]/1000},{proc_temp["processor_temperature"]/100},{pcb_temp["pcb_temperature"]/100}\n')
        time.sleep(2.0 - ((time.time() - starttime) % 2.0))                     ### <- set the timeinterval for repetition of loop


except KeyboardInterrupt:
    print("Keyboard break")
except Exception as err:
    print(err)
    sys.exit()
