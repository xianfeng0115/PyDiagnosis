
import ctypes, os

class QLib(object):
    def __init__(self):
        p = os.path.join(__file__[0:__file__.find('\\qlib')], 'QMSL_MSVC6R.dll')
        self._dll = ctypes.CDLL(p)
        self._handle = 0
    
    def connect(self):
        self._handle = self._dll.QLIB_ConnectServer(0xffff)
    
    def offline(self):
        self._dll.QLIB_DIAG_CONTROL_F(self._handle, 1)
    
    def online(self):
        self._dll.QLIB_DIAG_CONTROL_F(self._handle, 4)
    
    def reset(self):
        self._dll.QLIB_DIAG_CONTROL_F(self._handle, 2)
    
    def disconnect(self):
        self._dll.QLIB_DisconnectServer(self._handle)
    
    def poweroff(self):
        self._dll.QLIB_DIAG_CONTROL_F(self._handle, 6)
        
    def lowpower(self):
        self._dll.QLIB_DIAG_CONTROL_F(self._handle, 5)
