# coding:utf-8
import serial
import time
from API.Serial import *

class ATHandle(SerialHandle):

    def login(self):
        pass

    def send_com_sigle(self, cmd):
        time.sleep(0.1)
        self.ser.write(self.encode(cmd))
        time.sleep(1)
        result = self.decode(self.ser.readall())
        result = result + self.decode(self.ser.read(self.ser.inWaiting()))
        return result


    def send_data(self, cmd):
        self.ser.write(self.encode(cmd))

if __name__ == '__main__':
    serclass = ATHandle('COM21')
    print(serclass.send_com_sigle('ati\r\n'))