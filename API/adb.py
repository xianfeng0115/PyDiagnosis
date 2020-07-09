# -*- coding: UTF-8 -*-
'''
Created on 2016-03-16

@author: bogen
'''
import subprocess
import logging
import threading

class ADB:
    def __init__(self, osLocation="adb"):
        self.mAdbOsLocation = osLocation
        pass
    
    def _exec(self, cmd, device=None):
        arg = list(cmd)
        
        if device:
            arg[0:0]=[self.mAdbOsLocation, "-s", device]
        else:
            arg.insert(0, self.mAdbOsLocation)
        print(arg)
        si = subprocess.STARTUPINFO()
        si.wShowWindow =subprocess.SW_HIDE
        process = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, startupinfo=si)
        errorOutput = []
        stdOutput = []
        status = self.grabProcessOutput(process, errorOutput, stdOutput, False)
        return status, "".join(stdOutput)
    
    def cmd(self, cmd, device=None):
        return self._exec(cmd, device);
        
    def shell(self, cmd, device=None):
        return self._exec(["shell", cmd], device)
    
    def push(self, deviceFile, localFile, device=None):
        return self._exec(["push", localFile, deviceFile], device)
    
    def pull(self, deviceFile, localFile, device=None):
        return self._exec(["pull", deviceFile, localFile], device)
    
    def forwardPort(self, devicePort, localPort, device=None):
        return self._exec(["forward", "tcp:"+str(localPort), "tcp:"+str(devicePort)], device)
    
    def cmd_asy(self, cmd, device):
        arg = list(cmd)
        if device:
            arg[0:0]=[self.mAdbOsLocation, "-s", device]
        else:
            arg.insert(0, self.mAdbOsLocation)
        si = subprocess.STARTUPINFO()
        si.wShowWindow =subprocess.SW_HIDE
        #popen = subprocess.Popen(["dir", '.'], shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        #o = open("output/fd.txt", 'w+')
        print(arg)
        return subprocess.Popen(arg, stdout=None, stderr=None, shell=False, startupinfo=si)
    
    def listDevices(self):
        ret = self.cmd(["devices"])
        if ret[0]!=0:
            return []
        devices=[]
        for i in ret[1].split('\r\n'):
            if i.endswith("\tdevice"):
                devices.append(i.split()[-2])
        return devices
    
    def startAdb(self):
        arg = [self.mAdbOsLocation, "start-server"]
        si = subprocess.STARTUPINFO()
        si.wShowWindow =subprocess.SW_HIDE
        process = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, startupinfo=si)
        errorOutput = []
        stdOutput = []
        status = self.grabProcessOutput(process, errorOutput, stdOutput, False)
        if status != 0:
            raise Exception()
        
    def stopAdb(self):
        arg = [self.mAdbOsLocation, "kill-server"]
        si = subprocess.STARTUPINFO()
        si.wShowWindow =subprocess.SW_HIDE
        process = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, startupinfo=si)
        status = process.wait()
        if status != 0:
            raise Exception()

    def grabProcessOutput(self, process, errorOutput, stdOutput, waitForReaders):
        def readError():
            while True:
                nl = process.stderr.readline()
                if not nl:
                    return
                errorOutput.append(nl.decode(encoding='ISO-8859-1'))
                
        def readOut():
            while True:
                nl = process.stdout.readline()
                if not nl:
                    return
                stdOutput.append(nl.decode(encoding='ISO-8859-1'))
                    
        t1 = threading.Thread(target=readOut)
        t2 = threading.Thread(target=readError)
        t1.setDaemon(True)
        t2.setDaemon(True)
        t1.start()
        t2.start()
        if waitForReaders:
            t1.join()
            t2.join()
        return process.wait()

if __name__ == '__main__':
    adb = ADB()
    back = adb.startAdb()
    adb.cmd('adb shell uname -a')
    pass