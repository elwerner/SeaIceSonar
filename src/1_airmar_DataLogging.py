# -*- coding: utf-8 -*-
'''
#######################################
# Operating Echosounders Icelab
#
# @author: Ellen Werner 
ellen.werner@hcu-hamburg.de
# date: 24.06.2022
# Data Logging with Airmar sonar 
#######################################
'''

### imports
import serial
import sys
import time
import datetime

### Intitialize airmar via serial connection
try:
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

    ### Set instrument configuration
    
    
    myAirmarIn.write('$PAMTC,OPTION,SET,PING,ON\r\n'.encode('ascii'))           # start Pinging
    time.sleep(5) 
    myAirmarIn.write('$PAMTC,OPTION,SET,OUTPUTMC\r\n'.encode('ascii'))          # Change nmea output settings to: NMEA depth output after each ping 
    myAirmarIn.write('$PAMTC,OPTION,SET,PING,OFF\r\n'.encode('ascii'))          # stop Pinging
    myAirmarIn.write('$PAMTC,EN,MTW,0\r\n'.encode('ascii'))                     # Stop output of MTW data (so only DPT data is output)
    myAirmarOut.flushInput()


    ### Reading the data from sensor 

     
    starttime=time.time()
    while True:
        # myAirmarIn.write('$PAMTC,OPTION,SET,PING,ONCE\r\n'.encode('ascii'))
        
        myAirmarIn.write('$PAMTC,OPTION,SET,PING,ON\r\n'.encode('ascii'))       # start Pinging for 1sec
        myAirmarOut.flushInput()
        time.sleep(1)                                                                               
        
        nmea = myAirmarOut.readline()                                           # read out nmea data 
        nmea = nmea.strip().decode('ascii', errors='replace')
        timestamp = str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))  # create timestamp
        print(f'{timestamp},{nmea}')                                            # print to terminal
        myAirmarIn.write('$PAMTC,OPTION,SET,PING,OFF\r\n'.encode('ascii'))      # stop Pinging
        
        ## Save measurements in a csv-file
        #with open(f'DataLogs/AirmarLog_{timestamp[0:10]}.csv', 'a') as f:       ### <- EDIT FILENAME HERE
            #f.write(f'{timestamp},{nmea}\n')
        
        time.sleep(5.0 - ((time.time() - starttime) % 5.0))                     ### <- set the timeinterval for repetition of loop

    myAirmarIn.close()
    myAirmarOut.close()  
               

except serial.SerialException as err:
    print("Serial Port Error: \n" + str(err))
    sys.exit()
except KeyboardInterrupt:
    print("Keyboard break")
    myAirmarIn.close()
    myAirmarOut.close()
except Exception as err:
    print(err)
    sys.exit()
    


