# coding:utf-8
import serial
from Common.CommonVar import *
import time

class SerialHandle:
    """
        串口通信
    """

    def __init__(self, com_port, bps=115200, timeout=1):
        self.ser = self.set_serial(com_port, bps, timeout)

    def set_serial(self, com_port, bps, timeout):
        ser = serial.Serial(com_port, bps, timeout=timeout)
        return ser

    def login(self):
        while 1:
            self.ser.write(self.encode('\n'))
            result = self.ser.readline()
            if b'login'in result:
                s = self.ser.write(self.encode('root\n'))
                time.sleep(0.1)
                s = self.ser.write(self.encode('Dgyus@312893\n'))
            elif b'iBox:' in result:
                self.ser.readlines()
                return True
    def send_com_sigle(self, cmd):
        self.ser.flushOutput()
        time.sleep(0.1)
        self.ser.write(self.encode(cmd))
        result = self.decode(self.ser.read_until('root@iBox:~#'))
        return result

    def decode(self, str):
        if type(str) is bytes:
            return str.decode("ISO-8859-1")
        return str

    def encode(self, str):
        if type(str) is not bytes:
            try:
                return str.encode("ISO-8859-1")
            except:
                return str
        return str

if __name__ == '__main__':
    serclass = SerialHandle('COM12')
    serclass.login()
    print(serclass.send_com_sigle('pwd\n'))