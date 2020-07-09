
#import sys
#
#if sys.platform.startswith('win'):
#    from windows._keyboard import sendkeys, keydown, keyup
#    from windows._mouse import click, doubleclick, rightclick, mousemove     
#elif sys.platform.startswith('darwin'):
#    from mac._keyboard import sendkeys, keydown, keyup
#else:
#    from linux._keyboard import sendkeys, keydown, keyup
#
#class _Keyboard(object):
#    def __init__(self, sendkeys, keydown, keyup):
#        self.sendkeys = sendkeys
#        self.keydown = keydown
#        self.keyup = keyup
#
#class _Mouse(object):
#    
#    def __init__(self,click, doubleclick, rightclick, mousemove):
#        self.click = click
#        self.doubleclick = doubleclick
#        self.rightclick = rightclick
#        self.mousemove = mousemove
#        pass
#
#keyboard = _Keyboard(sendkeys, keydown, keyup)
#mouse = _Mouse(click, doubleclick, rightclick, mousemove)
