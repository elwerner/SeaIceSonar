#######################################
# Operating Echosounders Icelab
# @author: Ellen Werner 
# ellen.werner@hcu-hamburg.de
# date: 08.06.2022
# Checking for serial ports available
#######################################


import serial
ports = []
for port in range(1,256):
    try:
        s = serial.Serial(f'COM{port}')
        s.close()
        ports.append(f'COM{port}')
    except serial.SerialException: 
        pass

print(ports)
