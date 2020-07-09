# -*- coding: utf-8 -*-
import os, sys, types
import subprocess
import logging, random
import serial
import time, re, threading
from powerlib.usbcontroller import Usb as USBController
from adb import ADB

try:
    import queue
except ImportError:
    import Queue as queue

ARDUINO_COM = "COM11"#Arduino的端口号，在设备管理器中一般叫做USB-SERIAL CH340
KL15_RELAY = "2"#控制KL15的继电器，如果使用测试板控制KL15，无需配置
KL30_RELAY = '1'#控制KL30的继电器
USB_RELAY='4'#控制USB连线的继电器
LK15_CONTROL_COM = "COM5"#测试板的端口号
SERIAL_LOG_COM = "COM4"#抓取串口log的端口号
TBOX_IP="192.168.225.1"#TBOX NDIS的IP地址
TBOX_DIAG_KEY="41A1E8E24430B160F9D2A0B5F79BADE3F23061F33F0FB6C8F483691A578A9DBF0446D7DEBA4598F4372B9FB53FBE3481411D2151AD183500BF33233CD1A5E9840C0D004BCB77DA38A0FD8F7E3FFF4CCA171BAFEFE740C12BA607104ACDCFCF4A43C1B873FF2C10D6263AEABE7976F78E267465BC57D6C8EDB77A270774BEDD0092C724AD8966580BAAE161B70D1AE6CCB23A859791D3CA07E6F2D44FB548274987F1BDAD4CE60863CD53969C0522434A797E79F56C45357DE19CCC369D899A041002516BCBBE938CD567C6177120A1BCF248B37CFC6800D2BD0ABBFCEA51828162B55571849C1691A855D1812C3F1BB643E768584AE7F6096F9CF891D6BF3AD3"#切到诊断模式的秘钥
TBOX_ADB_SN="1234567890ABCDEF"#TBOX的ADB序号
PHONE_SUPPORT_TEST_SN="7140417"#辅测手机的ADB序号
TBOX_PHONE_NUM="18494712804"#TBOX的电话号码
LOGPATH="output"#log保存的目录
CLOSE_WORKING_TIME = 2*60 #无csp业务进入Standy或Sleep的时间
STANDBY_MAXTIME = 2*60 #Standy的持续时间
SLEEP_POOL_MAXTIME1 = 3*60 #Sleep1的持续时间
SLEEP_POOL_MAXTIME2 = 3*60 #Sleep2的持续时间
SLEEP_POLL_INTERVAL1 = 1*60 #Sleep1的唤醒周期
SLEEP_POLL_INTERVAL2 = 1*60 #Sleep2的唤醒周期


class PowerUsbController():
    def __init__(self):
        self.arduino = serial.Serial(ARDUINO_COM, baudrate=9600, bytesize=8,parity='N',stopbits=1,xonxoff=False, timeout=20)
        time.sleep(2)
        
    def SHUTDOWN_KL15(self, com=LK15_CONTROL_COM):
        t = serial.Serial(com, baudrate=115200, bytesize=8,parity='N',stopbits=1,xonxoff=0, timeout=1)  
        n = t.write('\x4B\xEF\x0E\x00\x0A\xF3\x7E')
        logging.info("shutdown KL15")
        time.sleep(1)
        print ''.join('\\x%.2x' % ord(x) for x in t.read(8))
    def OPEN_KL15(self, com=LK15_CONTROL_COM):
        t = serial.Serial(com, baudrate=115200, bytesize=8,parity='N',stopbits=1,xonxoff=0, timeout=1)  
        n = t.write('\x4B\xEF\x12\x00\x3B\xCF\x7E')
        logging.info("open KL15")
        time.sleep(1)
        print ''.join('\\x%.2x' % ord(x) for x in t.read(8))
        
    
    # def SHUTDOWN_KL15(com=ARDUINO_COM, relay=KL15_RELAY):
        # logging.info("shutdown KL15")
        # n = t.write('close'+relay+'\r')
        # t.read(6)
        # time.sleep(2)
    # def OPEN_KL15(com=ARDUINO_COM, relay=KL15_RELAY):
        # logging.info("open KL15")
        # n = t.write('open'+relay+'\r')
        # time.sleep(2)
        # t.read(5)
        
    def OPEN_MAIN_POWER(self, com=ARDUINO_COM, relay=KL30_RELAY):
        logging.info("open KL30")
        n = self.arduino.write('open'+relay+'\r') 
        self.arduino.read(5)
        time.sleep(2)
        
    def CLOSE_MAIN_POWER(self, com=ARDUINO_COM, relay=KL30_RELAY):
        logging.info("shutdown KL30")
        n = self.arduino.write('close'+relay+'\r')
        self.arduino.read(6)
        time.sleep(2)
        
    def USB_ON(self, com=ARDUINO_COM, relay=USB_RELAY):
        logging.info("USB ON")
        #t = serial.Serial(com, baudrate=9600, bytesize=8,parity='N',stopbits=1,xonxoff=False, timeout=1)
        n = self.arduino.write('open'+relay+'\r')
        #n = t.write('open'+relay+'\r\n')
        time.sleep(2)
        self.arduino.read(5)
        time.sleep(2)
        
    def USB_OFF(self, com=ARDUINO_COM, relay=USB_RELAY):
        logging.info("USB OFF")
        #t = serial.Serial(com, baudrate=9600, bytesize=8,parity='N',stopbits=1,xonxoff=False, timeout=1)
        n = self.arduino.write('close'+relay+'\r')
        #n = t.write('close'+relay+'\r\n')
        time.sleep(2)
        self.arduino.read(6)
        
class ComLog():
    def __init__(self):
        self.modeSwitchCallback = None
        self.logFile = SERIAL_LOG_PATH
        self.currentMode = ''
        self.stopMonitor = False
        self.statQueue = queue.Queue(1024)
        self.statEvent=threading.Event()
        
    def startMonitorLog(self):
        t1 = threading.Thread(target=self.moitorLog)
        t1.setDaemon(True)
        t1.start()
        #t1.join()
        self.stopMonitor = False
        
    def stopMonitorLog(self):
        self.stopMonitor = True
        self.t.cancel_read()
        self.t.close()
        
    def setModeSwitchCallback(self, modeSwitchCallback):
        self.modeSwitchCallback  = modeSwitchCallback
        
    def waitNextStat(self, expect=None, timeout=1200):
        leftTime = timeout
        startTime = time.time()
        while leftTime>0:
            try:
                stat = self.statQueue.get(True, leftTime)
            except:
                if expect:
                    raise Exception("power status is not changed to " + str(expect) + " in " + str(timeout) +"s")
                else:
                    raise Exception("power status is not changed in " + str(timeout) +"s")
            if not expect:
                return stat
            elif expect==stat[1]:
                return stat
            leftTime = timeout-time.time()+startTime
        
        
    def clearStatQueue(self):
        while not self.statQueue.empty():
            try:
                self.statQueue.get()
            except:
                break
        
    def moitorLog(self):
        self.t = serial.Serial(SERIAL_LOG_COM, baudrate=115200,bytesize=7,parity='O',stopbits=1,xonxoff=0, timeout=3)
        logFile = open(self.logFile, 'a')
        LOG_WORKING='PM5,W'
        LOG_STANDBY='PM39'
        LOG_SLEEP1='PM12,2S1'
        LOG_SLEEP2='PM14,2S2'
        LOG_OFF='PM17,2OF'
        LOG_STORAGE='PM37'
        MODE_SWITH_RE = re.compile(r'\s*\[mode_switch\]\s*switching  to \[(.*)\] !')
        currentMode = ''
        while not self.stopMonitor:
            a = self.t.readline()
            if not a:
                continue
            #sys.stdout.write(a)
            logFile.write(time.strftime('[%m-%d %H:%M:%S]',time.localtime(time.time())))
            logFile.write(a)
            logFile.flush()
            m = MODE_SWITH_RE.match(a)
            if a.startswith(LOG_WORKING):
                currentMode = 'working'
            elif a.startswith(LOG_STANDBY):
                currentMode = 'Standby'
            elif a.startswith(LOG_SLEEP1):
                currentMode = 'Sleep1'
            elif a.startswith(LOG_SLEEP2):
                currentMode = 'Sleep2'
            elif a.startswith(LOG_OFF):
                currentMode = 'Off'
            elif a.startswith(LOG_STORAGE):
                currentMode = 'storage'
            elif "Initialize the tbox..." in a and self.currentMode=="working":
                logging.error("Maybe reboot, find 'Initialize the tbox...' and current mode is working!")
                #catchSysLog()
                sys.exit()
            elif "Initialize the tbox..." in a:
                currentMode = "Init"
            elif "Fault_Handler" in a:
                logging.error("Maybe reboot, find 'Fault_Handler'!")
                #catchSysLog()
                sys.exit()
            elif "WWDG_IRQHandlerzte" in a:
                logging.error("Maybe reboot, find 'WWDG_IRQHandlerzte'!")
                #catchSysLog()
                sys.exit()
            
            if self.currentMode != currentMode:
                self.statQueue.put((time.time(), currentMode))
                logging.info("[mode_switch] from " + self.currentMode + " to " + currentMode)
                self.currentMode = currentMode
                if self.modeSwitchCallback:
                    self.modeSwitchCallback(currentMode)
            
                
def openADB(ip, key):
    exepath = os.path.join(os.path.dirname(__file__), 'Y100X_debug.exe')
    p = subprocess.Popen(exepath, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    time.sleep(1)
    c = p.communicate("192.168.225.1\r\n41A1E8E24430B160F9D2A0B5F79BADE3F23061F33F0FB6C8F483691A578A9DBF0446D7DEBA4598F4372B9FB53FBE3481411D2151AD183500BF33233CD1A5E9840C0D004BCB77DA38A0FD8F7E3FFF4CCA171BAFEFE740C12BA607104ACDCFCF4A43C1B873FF2C10D6263AEABE7976F78E267465BC57D6C8EDB77A270774BEDD0092C724AD8966580BAAE161B70D1AE6CCB23A859791D3CA07E6F2D44FB548274987F1BDAD4CE60863CD53969C0522434A797E79F56C45357DE19CCC369D899A041002516BCBBE938CD567C6177120A1BCF248B37CFC6800D2BD0ABBFCEA51828162B55571849C1691A855D1812C3F1BB643E768584AE7F6096F9CF891D6BF3AD3\r\n")
    if c[0]:
        logging.info(str(c[0]))
    if c[1]:
        logging.info(str(c[1]))

def catchSysLog():
    powerUsbController.OPEN_MAIN_POWER()
    powerUsbController.OPEN_KL15()
    powerUsbController.USB_ON()
    time.sleep(20)
    logging.info("swith to Diagnostics Mode")
    openADB(TBOX_IP, TBOX_DIAG_KEY)
    time.sleep(20)
    adb = ADB()
    logPath = os.path.join(LOG_DIR, time.strftime('sysLog-%m-%d-%H_%M_%S',time.localtime(time.time())))
    adb.pull('/logfs', logPath, TBOX_ADB_SN)
    
def init():
    global LOG_DIR
    LOG_DIR = os.path.join(LOGPATH, time.strftime('%m-%d-%H_%M_%S',time.localtime(time.time())))
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    global SERIAL_LOG_PATH
    global LOG_PATH
    SERIAL_LOG_PATH = os.path.join(LOG_DIR, "serial.log")
    LOG_PATH = os.path.join(LOG_DIR, "this.log")
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_PATH,
                    filemode='w')

    #################################################################################################
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)-6s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    global log
    log = ComLog()
    log.startMonitorLog()
    global powerUsbController
    powerUsbController = PowerUsbController()

def loopInit():
    powerUsbController.OPEN_MAIN_POWER()
    powerUsbController.OPEN_KL15()
    powerUsbController.USB_ON()
    time.sleep(20)
    logging.info("swith to Diagnostics Mode")
    openADB(TBOX_IP, TBOX_DIAG_KEY)
    time.sleep(20)
    powerUsbController.SHUTDOWN_KL15()
    time.sleep(2)
    adb = ADB()
    #adb.stopAdb()
    #adb.startAdb()
    logging.info("adb shell zte_topsw_mcutest 29 02000600060002000200020004000000")
    ret = adb.shell("zte_topsw_mcutest 29 02000600060002000200020004000000", TBOX_ADB_SN)
    if(0 != ret[0]):
        raise Exception("send adb shell zte_topsw_mcutest failed! " + ret[2])
    logging.info(ret[1])
    time.sleep(1)


def loop_Only_Sleep_KL15():
    """仅测试sleep，然后打开KL15"""
    logging.info("This loop: open KL15 when " + stat_open_KL15)
    powerUsbController.OPEN_MAIN_POWER()
    powerUsbController.OPEN_KL15()
    powerUsbController.USB_OFF()
    log.clearStatQueue()
    stat = log.waitNextStat(None, 1200)
    if stat[1] != "Init":
        raise Exception("open KL15 cannot find 'Initialize the tbox...' in log")
        
    powerUsbController.SHUTDOWN_KL15()
    stat = log.waitNextStat(None, 1200)
    if stat[1] != "Sleep1":
        raise Exception("After shutdown KL15, it should into sleep1")
    
        
        

init()
powerUsbController.CLOSE_MAIN_POWER()
powerUsbController.SHUTDOWN_KL15()
powerUsbController.USB_OFF()
try:
    for i in xrange(999990):
        logging.info("start loop " + str(i+1))
        loop_Only_Sleep_KL15
        logging.info("end loop " + str(i+1))
        logging.info('================================================================================\n\n\n')
        time.sleep(10)
except Exception,e:
    logging.error(str(e))
log.stopMonitorLog()
print "End!"