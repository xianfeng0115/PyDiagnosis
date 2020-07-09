#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Document: network script, keep network always working, using python3"""

import os
import sys
import time
import logging, random
import subprocess
from adb import ADB

PING_RESULT = 0
NETWORK_RESULT = 0
LOGPATH = "output"       # log保存的目录

def DisableNetwork():
    ''' disable network card '''
    result = os.system(u"netsh interface set interface 以太网 disable")
    if result == 1:
        print("disable network card failed")
    else:
        print("disable network card successfully")

def ping():
    trytime = 30
    success = 0
    adb = ADB()
    cmd = "ping -c 4 {0} | grep -q 'ttl=' && echo '{0} ok' || echo '{0} failed'".format('61.135.169.125')
    print(cmd)
    for i in range(trytime):
        result = adb.shell(cmd)
        if 'ok' in result[1]: success += 1
        print(result)
    return success





def init():
    time.sleep(5)
    logPath = os.path.join(LOGPATH, time.strftime('%m-%d-%H_%M_%S',time.localtime(time.time())))
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    global SERIAL_LOG_PATH
    global LOG_PATH
    SERIAL_LOG_PATH = os.path.join(logPath, "serial.log")
    LOG_PATH = os.path.join(logPath, "this.log")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S', filename=LOG_PATH, filemode='w')


if __name__ == '__main__':

    logging.info("Start Test!")
    print(ping())
    # while True:
    #     PING_RESULT = ping()
    #     if PING_RESULT == 0:
    #         time.sleep(20)
    #     else:
    #         logging.error(time.clock(),"Ping fail")
    #         DisableNetwork()
    #         time.sleep(10)
