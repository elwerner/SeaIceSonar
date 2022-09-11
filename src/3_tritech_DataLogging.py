# -*- coding: utf-8 -*-
'''
#######################################
Operating Echosounders Icelab

@author: Ellen Werner 
ellen.werner@hcu-hamburg.de
date: 10.07.2022
Data Logging with Tritech sonar
#######################################
'''

### imports
import serial
import sys
import time
import datetime

### Intitialize tritech via serial connection
try:
    myTritech = serial.Serial(
    port='COM52',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

    print("------------------------------------")
    print("Tritech connected at: " + myTritech.name)
    print("starting Tritech...")

    ### Set measurement parameters on the sensor
    
    myTritech.write(b'Z')                      # Change the mode from free running to interrogate mode


    ### Reading the data from sensor 


    starttime=time.time()
    while True:
        myTritech.write(b'Z')                                                   # trigger one ping
        
        data = myTritech.readline()                                             # read out data 
        data = data.strip().decode()
        timestamp = str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))  # create timestamp
        print(f'{timestamp},{data}')                                            # print to terminal
        
        ## Save measurements in a csv-file
        with open(f'DataLogs/TritechLog_{timestamp[0:10]}.csv', 'a') as f:      ### <- EDIT FILENAME HERE
            f.write(f'{timestamp},{data}\n')
        time.sleep(6.0 - ((time.time() - starttime) % 6.0))                     ### <- set the timeinterval for repetition of loop
               
    myTritech.close()

except serial.SerialException as err:
    print("Serial Port Error: \n" + str(err))
    sys.exit()
except KeyboardInterrupt:
    print("Keyboard break")
    myTritech.close()
except Exception as err:
    print(err)
    sys.exit()
    


