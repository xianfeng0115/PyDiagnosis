import os
import time
import serial
import serial.tools.list_ports


def shutdownKL15(com):
    t = serial.Serial(com, baudrate=115200, bytesize=8,parity='N',stopbits=1,xonxoff=0, timeout=1)  
    n = t.write('\x4B\xEF\x0E\x00\x0A\xF3\x7E')
    time.sleep(1)
    print t.read(8)
def openKL15(com):
    t = serial.Serial(com, baudrate=115200, bytesize=8,parity='N',stopbits=1,xonxoff=0, timeout=1)  
    n = t.write('\x4B\xEF\x12\x00\x3B\xCF\x7E')
    time.sleep(1)
    print t.read(8)
    
for i in range(1,5):
    #shutdownKL15("COM43")
    #time.sleep(5)
    openKL15("COM43")
    #time.sleep(5)