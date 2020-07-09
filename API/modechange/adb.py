# -*- coding: UTF-8 -*-
'''
Created on 2016-03-16

@author: bogen
'''
import subprocess
import logging
import threading
import os, sys, time

class ADB:
    def __init__(self, osLocation="adb"):
        if not osLocation:
            osLocation = "adb"
        self.mAdbOsLocation = osLocation
        pass
    
    def _exec(self, cmd, device=None):
        arg = list(cmd)
        if device:
            arg[0:0]=[self.mAdbOsLocation, "-s", device]
        else:
            arg.insert(0, self.mAdbOsLocation)
        process = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errorOutput = []
        stdOutput = []
        status = self.grabProcessOutput(process, errorOutput, stdOutput, True)
        return status, "".join(stdOutput), "".join(errorOutput)
    
    def cmd(self, cmd, device=None):
        if isinstance(cmd, basestring):
            cmd = [cmd]
        return self._exec(cmd, device);
        
    def shell(self, cmd, device=None):
        if isinstance(cmd, basestring):
            return self.cmd(["shell", cmd], device)
        else:
            arg = list(cmd)
            arg.insert(0, "shell")
        return self.cmd(arg, device)

    
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
        #popen = subprocess.Popen(["dir", '.'], shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        #o = open("output/fd.txt", 'w+')
        return subprocess.Popen(arg, stdout=None, stderr=None)
    
    def listDevices(self):
        ret = self.cmd(["devices"])
        if ret[0]!=0:
            return []
        devices=[]
        for i in ret[1].split(os.linesep):
            if i.endswith("\tdevice"):
                devices.append(i.split()[-2])
        return devices
    
    def waitForDevice(self, id, timeout):
        startTime = time.time()
        while True:
            if id and id in self.listDevices():
                return
            if not id and len(self.listDevices())>0:
                return
            if time.time()-startTime>timeout:
                raise Exception("timeout, failed to wait for device")
    
    def startAdb(self):
        arg = [self.mAdbOsLocation, "start-server"]
        process = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errorOutput = []
        stdOutput = []
        status = self.grabProcessOutput(process, errorOutput, stdOutput, False)
        if status != 0:
            raise Exception()
        
    def stopAdb(self):
        arg = [self.mAdbOsLocation, "kill-server"]
        process = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = process.wait()
        if status != 0:
            raise Exception()

    def grabProcessOutput(self, process, errorOutput, stdOutput, waitForReaders):
        def readError():
            while True:
                nl = process.stderr.readline()
                if not nl:
                    return
                errorOutput.append(nl)
                
        def readOut():
            while True:
                nl = process.stdout.readline()
                if not nl:
                    return
                stdOutput.append(nl)
                    
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
        