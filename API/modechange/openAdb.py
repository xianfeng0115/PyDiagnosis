# -*- coding: utf-8 -*-
import zeus.gui.win as zeus
import time

class MainApp(object):    
    def __init__(self, path, arg=[], timeout = 3):
        win = zeus.WinDriver()
        win.open(path, 0, arg)
        time.sleep(timeout) 
        self.element = win.main
        self.app = win
        
    def tap_Execute_the_command(self):
        self.element.Button(name="Execute the command").click()
        time.sleep(1)
        
    def tap_Close(self):
        self.element.Button(name="Close").click()
        time.sleep(0.5)
    
    def quit(self):
        self.app.quit()

     
def openADB(id):
    tool = MainApp("C:\\Program Files (x86)\\Bus Hound\\buscmdr.exe", ["-"+str(id)])
    tool.tap_Execute_the_command()
    tool.quit()
    
if __name__ == '__main__':
    tool = MainApp("C:\\Program Files (x86)\\Bus Hound\\buscmdr.exe", ["-14"])
    tool.tap_Execute_the_command()
    tool.quit()
    #time.sleep(4)
    