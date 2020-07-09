#import platform
from ctypes import CDLL


#class PlatformBits(object):
#    def __init__(self):
#        self.__sysbits = platform.architecture()
#        pass
#        
#    def getsystembits(self):
#        if self.__sysbits[0].find('32') != -1:
#            return "32"
#        elif self.__sysbits[0].find('64') != -1:
#            return "64"
#        else:
#            raise Exception("Usb driver doesn't support")

import os
class Usb(object):
    def __init__(self):        
        p = os.path.join(__file__[0:__file__.find('\\usbcontroller')], 'Control_USB.dll')        
        self.__dllhandle = CDLL(p)
        self.__poweron = self.__dllhandle.Open_Switch_Board
        self.__poweron.argtypes = []
        self.__poweron.restype  = None
        
        self.__poweroff = self.__dllhandle.Close_Switch_Board
        self.__poweroff.argtypes = []
        self.__poweron.restype = None
    
    def poweron(self):
        self.__poweron()
        
    def poweroff(self):
        self.__poweroff()
    
if __name__ == '__main__':
    usb = Usb()
    #usb.poweroff()
    
    usb.poweron()

