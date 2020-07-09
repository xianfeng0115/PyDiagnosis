# -*- coding: utf-8 -*-
import os, sys, types
import logging, random
import serial
#import paramiko
import time
from contextlib import suppress
from modechange import *
import subprocess

'''测试脚本用于针对Ibox项目电源接口进行压力测试
从MPU ping外网。从AG35 USB ping外网。MPU连接司南后的正常频率吐数据'''
try:
    import queue
except ImportError:
    import Queue as queue

IBOX_AT_COM = "COM15"     # 测试样件的AT端口号
IBOX_Derial_COM = "COM8"    # 测试样件的Diagnostics端口号
ARDUINO_COM = "COM5"    # Arduino的端口号，在设备管理器中一般叫做USB-SERIAL CH340
SWITCH_RELAY = '3'        # 控制开关机按钮的继电器
RESET_RELAY = '2'        # 控制RESET的继电器
USB_RELAY = '1'            # 控制USB连线的继电器
baudRate = 9600  # 波特率

LOGPATH = "output"       # log保存的目录
RandomNum = 0           # 100以内随机数生成
RESET_SHORT_TIME =140    # 短按reset按键时间长度，单位：秒
RESET_SHORT_RANGE = 30   # 短按reset按键时间长度范围，单位：秒
RESET_LONG_TIME = 8     # 长按reset按键时间长度，单位：秒
RESET_LONG_RANGE = 565    # 长按reset按键时间长度，单位：秒565
WAITTING_TIME = 30      # 等待开机并出现AT端口，单位：秒


t = serial.Serial(ARDUINO_COM, baudrate=baudRate, bytesize=8, parity='N', stopbits=1, xonxoff=False, timeout=20)
'''
    控制继电器进行开关操作
'''

class IboxSwitch():
    def KL30_off(self):
        relay = USB_RELAY
        time.sleep(3)
        logging.info("Turn Off")
        print("Turn off")
        t.write(('open' + str(relay) + '\r').encode())

    def KL30_on(self):
        relay = USB_RELAY
        time.sleep(3)
        logging.info("Turn On")
        print("Turn On")
        t.write(('close' + str(relay) + '\r').encode())
    def usb_off(self):
        relay = RESET_RELAY
        time.sleep(3)
        logging.info("Turn Off")
        print("Turn off")
        t.write(('open' + str(relay) + '\r').encode())

    def usb_on(self):
        relay = RESET_RELAY
        time.sleep(3)
        logging.info("Turn On")
        print("Turn On")
        t.write(('close' + str(relay) + '\r').encode())


'''
    向MPU的串口发送root已登录系统
'''
def root_start():
    s = serial.Serial(IBOX_Derial_COM, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, timeout=20)
    logging.info("root_start")
    # s.write(('\r\n').encode())
    print("start sleep 70")
    logging.info("start sleep 70")
    time.sleep(30)
    print("end sleep 70")
    logging.info("end sleep 70")
    print("等待出现开机关键字")
    result = s.read_until('Starting kernel', 100).decode('ISO-8859-1')
    if 'Starting kernel' in result :
        print("开机关键字已出现")
    time.sleep(45)
    print("root_start")
    s.write(('root' + '\r\n').encode())
    print(s.read(5))
    print("root_start")
    time.sleep(3)
    s.write(('Dgyus@312893' + '\r\n').encode())
    print(s.read(10).decode('ISO-8859-1'))
    logging.info("root_start")
    time.sleep(5)

'''
    向MPU的串口发送at命令，如果at端口正常则会有回复
'''
def check_at_com(self):
    s = serial.Serial(IBOX_Derial_COM, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, timeout=20)
    logging.info("check at com start")
    print("check at com")
    s.write(('root' + '\r').encode())
    print(self.port.read(5))
    time.sleep(5)
    s.write(('Dgyus@312893' + '\r').encode())
    print(self.port.read(5))
    logging.info("check at com end")
    logging.info("at com ok")

'''
    向MPU的串口发送ps命令，检查制定的ps进程是否已经启动
'''
def check_ps(psname,psnameall):
    s = serial.Serial(IBOX_Derial_COM, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, timeout=20)
    logging.info("check_ps")
    print("check_ps"+" ps -A | grep "+psname + '\r')
    s.write(('ps -A | grep '+psname + '\r').encode())
    result = s.read(80).decode('ISO-8859-1')
    time.sleep(10)
    # logging.info("result = "+ result)
    print("result = "+ result)
    if psnameall in result:
        return True
    else:
        return False


'''
    向MPU的串口发送ps命令，kill ps进程
'''
def kill_ps(psname):
    s = serial.Serial(IBOX_Derial_COM, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, timeout=20)
    logging.info("check_ps")
    print("kill_ps")
    s.write(('killall '+ psname + '\r').encode())

'''
    在给定的时间RESET_SHORT_TIME中，将MPU开机打印的串口信息记录下来，并且防止打印重复的log信息
'''
def read_date():
    s = serial.Serial(IBOX_Derial_COM, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, timeout=20)
    currenttime = time.time()
    print("currenttime=" + str(currenttime))
    data_bytesold = ''
    is_exit = False
    while not is_exit:
        print("while in=======")
        data_bytes = str(s.readline())
        if (data_bytesold != data_bytes):
            logging.info(str(data_bytes))
            data_bytesold = data_bytes

        if ((time.time() - currenttime) > RESET_SHORT_TIME):
            print("time.time()=" + str(time.time()))
            print("currenttime=" + str(currenttime))
            is_exit = True

'''
    从adb端口通过AG35模块ping外网，查看是否能够ping通外网
'''
def ping(pingaddr, count_all, count_sucess):
    success = 0
    adb = ADB()
    # cmd = "ping -c 1 {0} | grep -q 'ttl=' && echo '{0} ok' || echo '{0} failed'\n".format(pingaddr)
    cmd = "ping -c 1 {0}\n".format(pingaddr)

    for i in range(count_all):
        # result = adb.shell(cmd)
        # print(result)
        obj = subprocess.Popen(['adb', 'shell'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        obj.stdin.write(cmd.encode('utf-8'))
        obj.stdin.write('exit\n'.encode('utf-8'))  # 重点，一定要执行exit
        info, err = obj.communicate()

        if 'ttl=' in info.decode(): success += 1
        print(info)
    print(success)
    if success >= count_sucess :
        return 1
    return 0

'''
    从网口通过ssh登录到MPU进行ping操作，检查是否
    参数：
        targetAddr（ssh登录目标地址）,
        outAddr（需要ping的目的地址）,
        count（需要ping的次数）, 
        sername（ssh用户名）,
        password（ssh密码）
    返回值：true（全部ping通）  fault（部分失败）
'''
def sshManger(targetAddr,outAddr,count_all, count_sucess, username,password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if password is None:
        with suppress(paramiko.ssh_exception.SSHException):
            client.connect(targetAddr, port=22, username=username, password=password,allow_agent=False, look_for_keys=False)
        client.get_transport().auth_none(username)
    else:
        client.connect(targetAddr, port=22, username=username, password=password)

    ssh_shell = client.invoke_shell()
    ssh_shell.sendall('ping -c '+str(count_all)+' '+ outAddr + '\n')

    lines = []
    success = 0
    while True:
        line = ssh_shell.recv(1024).decode()
        print(line)
        lines.append(line)
        if 'ttl=' in line:
            success += 1
        if 'icmp_seq='+str(count_all) in line:
            break;
    result = ''.join(lines)
    print(result)
    if count_sucess >= count_sucess:
        return 1
    return 0

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


init()
# try:
#     for i in range(9999):
#         logging.info("============" + "start loop " + str(i+1) + "============")
#         print("============" + "start loop " + str(i+1) + "============")
#
#         if(check_ps('cv2x','cv2x-daemon')) :
#             assert (True,"检查到cv2x-daemon，运行成功")
#             print("检查到cv2x-daemon，运行成功")
#             logging.info("检查到cv2x-daemon，运行成功")
#         else:
#             print("没有检查到cv2x-daemon，运行失败")
#             logging.info("检查到cv2x-daemon，运行成功")
#             break
#         time.sleep(3)
#         kill_ps('dias_monitor_daemon.sh')
#         time.sleep(2)
#         kill_ps('diasdaemon')
#         time.sleep(2)
#
#         root_start()
#         if(check_ps('cv2x','cv2x-daemon')) :
#             assert (True,"检查到cv2x-daemon，运行成功")
#             print("检查到cv2x-daemon，运行成功")
#             logging.info("检查到cv2x-daemon，运行成功")
#         else:
#             print("没有检查到cv2x-daemon，运行失败")
#             logging.info("检查到cv2x-daemon，运行成功")
#             break
#
# except Exception as e:
#     logging.error(str(e))
logging.info("End!")
if __name__ == "__main__":
    iboxswitch=IboxSwitch()

    print("打开9")
    iboxswitch.usb_on()
    # usb_on(relay='9')
    print("打开8")
    iboxswitch.usb_off()

    time.sleep(10)


