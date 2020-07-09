'''
Created on 2011-12-26

@author: Administrator
'''
from ctypes import *
from ctypes.wintypes import *

class MOUSEINPUT(Structure):
    _fields_ = [("dx", LONG),
                ("dy", LONG),
                ("mouseData", DWORD),
                ("dwFlags", DWORD),
                ('time',DWORD),
                ('dwExtraInfo',POINTER(ULONG))
                ]
tagMOUSEINPUT = MOUSEINPUT

class KEYBDINPUT(Structure):
    _fields_ = [("wVk", WORD),
                ("wScan", WORD),                
                ("dwFlags", DWORD),
                ('time',DWORD),
                ('dwExtraInfo',POINTER(ULONG))
                ]
tagKEYBDINPUT = KEYBDINPUT

class HARDWAREINPUT(Structure):
    _fields_ = [("uMsg", DWORD),
                ("wParamL", WORD),                
                ("wParamH", WORD)                
                ]
tagHARDWAREINPUT = HARDWAREINPUT

class INPUT(Structure):
    class _INPUTUNION(Union):
        _fields_ = [("mi", MOUSEINPUT),
                    ("ki", KEYBDINPUT),                
                    ("hi", HARDWAREINPUT)            
                    ]
    
    _anonymous_ = ("union",)
    _fields_ = [("type", DWORD),
                ("union", _INPUTUNION)
                ]
tagINPUT = INPUT

class INPUTTYPE():
    MOUSE = 0
    KEYBOARD = 1
    HARDWARE = 2

class MOUSEEVENTFLAGS():
    ABSOLUTE = 0x8000
    HWHEEL = 0x01000
    MOVE = 0x0001
    MOVE_NOCOALESCE = 0x2000
    LEFTDOWN = 0x0002
    LEFTUP = 0x0004
    RIGHTDOWN = 0x0008
    RIGHTUP = 0x0010
    MIDDLEDOWN = 0x0020
    MIDDLEUP = 0x0040
    VIRTUALDESK = 0x4000
    WHEEL = 0x0800
    XDOWN = 0x0080
    XUP = 0x0100

class KEYEVENTFLAGS():
    EXTENDEDKEY = 0x0001
    KEYUP = 0x0002
    SCANCODE = 0x0008
    UNICODE = 0x0004

def throw_error_if_zero(handle):
    if handle == 0:
        raise WinError
    else:
        return handle

USER32 = WinDLL('user32.dll')
LPINPUT = POINTER(INPUT)
SendInput = USER32.SendInput
SendInput.argtypes = [UINT, LPINPUT, c_int]
SendInput.restype  = UINT

SetCursorPos = USER32.SetCursorPos
SetCursorPos.argtypes = [c_int,c_int]
SetCursorPos.restype = BOOL

GetSystemMetrics = USER32.GetSystemMetrics
GetSystemMetrics.argtypes = [c_int]
GetSystemMetrics.restype = c_int


#GetWindowText = USER32.GetWindowText
#GetWindowText.argtypes = [HWND, LPSTR, INT]
#GetWindowText.restype = INT
