import sys, os
import time
import serial
import serial.tools.list_ports

t = serial.Serial("com1", baudrate=115200,bytesize=7,parity='O',stopbits=1,xonxoff=0, timeout=1)
while True:
    a = t.readline();
    sys.stdout.write(a)
    if "mode" in a:
        sys.stdout.write(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time())))
        sys.stdout.write(a)