from _win32api  import SetCursorPos, SendInput, INPUT, MOUSEEVENTFLAGS, INPUTTYPE, GetSystemMetrics
from ctypes import pointer, sizeof

from zeus.osinput._util import ClickAction, MouseButton


def click(x, y, btn, act):    
    mousflags = MOUSEEVENTFLAGS.ABSOLUTE
    if btn == MouseButton.Right:
        mousflags = MOUSEEVENTFLAGS.RIGHTDOWN | MOUSEEVENTFLAGS.RIGHTUP | MOUSEEVENTFLAGS.ABSOLUTE        
    elif btn == MouseButton.Middle:
        mousflags = MOUSEEVENTFLAGS.MIDDLEDOWN | MOUSEEVENTFLAGS.MIDDLEUP | MOUSEEVENTFLAGS.ABSOLUTE
    else:
        mousflags = MOUSEEVENTFLAGS.LEFTDOWN | MOUSEEVENTFLAGS.LEFTUP | MOUSEEVENTFLAGS.ABSOLUTE
                
    input_structure = _buildparam(x, y, mousflags)    
    if act == ClickAction.DoubleClick:
        SendInput(1, pointer(input_structure), sizeof(input_structure))
        SendInput(1, pointer(input_structure), sizeof(input_structure))
    else:
        SendInput(1, pointer(input_structure), sizeof(input_structure))

def move(x, y):
    mousflags = MOUSEEVENTFLAGS.ABSOLUTE
    input_structure = _buildparam(x, y, mousflags)
    SendInput(1, pointer(input_structure), sizeof(input_structure))



SM_CXSCREEN = 0
SM_CYSCREEN = 1

cx = GetSystemMetrics(SM_CXSCREEN) - 3
cy = GetSystemMetrics(SM_CYSCREEN) - 3

XSCALEFACTOR = 65535 / (cx);
YSCALEFACTOR = 65535 / (cy);

def __buildparam(x, y, mousflags):
    x = x * XSCALEFACTOR
    y = y * YSCALEFACTOR
    
    input_structure = INPUT()
    input_structure.type = INPUTTYPE.MOUSE
    input_structure.union.mi.dx = x
    input_structure.union.mi.dy = y
    input_structure.union.mi.mouseData = 0
    input_structure.union.mi.dwFlags = mousflags
    return input_structure

def _buildparam(x, y, mousflags):    
    SetCursorPos(x, y)
    input_structure = INPUT()
    input_structure.type = INPUTTYPE.MOUSE
    input_structure.union.mi.dx = 0
    input_structure.union.mi.dy = 0
    input_structure.union.mi.mouseData = 0
    input_structure.union.mi.dwFlags = mousflags
    return input_structure




