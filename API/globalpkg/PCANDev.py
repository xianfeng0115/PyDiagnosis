from API.globalpkg.PCANBasic import *
import win32event
import time, datetime, os
import threading
from API.Logger import Loggers
logger = None
# if not logger:
#     log = Loggers(filename='AutoTest.log', log_dir='.', logtype='all')
#     logger = log.logger
from API.globalpkg.diagcandbc import DiagDict

class PCANDev():
    def __init__(self):
        self.m_objPCANBasic = PCANBasic()
        self.baudrate = PCAN_BAUD_500K
        self.m_PcanHandle = PCAN_USBBUS1
        try:
            result = self.m_objPCANBasic.Initialize(self.m_PcanHandle, self.baudrate)
            if result != PCAN_ERROR_OK:
                if result != PCAN_ERROR_CAUTION:
                    raise Exception('Error!', self.GetFormatedError(result))
            self.m_ReceiveEvent = win32event.CreateEvent(None, 0, 0, None)
            setResult = self.m_objPCANBasic.SetValue(self.m_PcanHandle, PCAN_RECEIVE_EVENT, self.m_ReceiveEvent)
            if setResult != PCAN_ERROR_OK:
                raise Exception('Error!', self.GetFormatedError(setResult))
        except Exception as e:
            logger.info('PCAN init failed:%s' %e)

    def GetFormatedError(self, error):
        stsReturn = self.m_objPCANBasic.GetErrorText(error, 0)
        if stsReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            return stsReturn[1]

    def WriteFrame(self, MsgDict):
        CANMsg = TPCANMsg()
        CANMsg.ID = int(MsgDict['ID'], 16)
        CANMsg.LEN = 8
        CANMsg.MSGTYPE = PCAN_MESSAGE_STANDARD
        for i in range(8):
            CANMsg.DATA[i] = int(MsgDict['DATA'][i], 16)
        # logger.info('发送消息%s:%s' % (MsgDict['ID'], MsgDict['DATA']))
        send_rst = self.m_objPCANBasic.Write(self.m_PcanHandle, CANMsg)
        # if CANMsg.ID == int('711', 16) or CANMsg.ID == int('6E1', 16):
        #     time.sleep(0.001)
        if send_rst != PCAN_ERROR_OK:
            logger.info(self.GetFormatedError(send_rst))

    def ReadFrame(self):
        msg = TPCANMsg()
        readRst = self.m_objPCANBasic.Read(self.m_PcanHandle)
        return readRst

    def close(self):
        releaseRst = self.m_objPCANBasic.Uninitialize(self.m_PcanHandle)
        if releaseRst == PCAN_ERROR_OK:
            logger.info("PCAN was successfully released")
        else:
            logger.info(self.GetFormatedError(releaseRst))

class ReadThread (threading.Thread):
    def __init__(self, pHandle):
        threading.Thread.__init__(self)
        self.PCAN = pHandle
        self.interrupt = False
        self.con = threading.Condition()
        self.read_mess = TPCANMsg()
        self.read_flag = True
        self.daemon = True
        nowtime = datetime.datetime.now()
        serlogdir = 'D:/3.gitlab/SAIC-AS28-TBOX_AUTO-TEST/interface_project_for_dev/logs/CAN/' + nowtime.strftime('%Y-%m-%d')
        if not os.path.exists(serlogdir):
            os.makedirs(serlogdir)
        serlogfile = serlogdir + '/CAN_' + nowtime.strftime('%H-%M-%S') + '.log'
        self.fp = open(serlogfile, 'w')

    def run(self):
        while self.read_flag:
            if self.interrupt:
                with self.con:
                    result = self.PCAN.ReadFrame()
                    if result[0] == PCAN_ERROR_OK:
                        self.read_mess = result[1]
                        msgID = hex(self.read_mess.ID)
                        msgData = []
                        for i in range(8):
                            msgData.append(hex(self.read_mess.DATA[i]))
                        self.fp.write('%s-----CHECK-----收到消息%s:%s\n' % (datetime.datetime.now(), msgID, msgData))
                        self.fp.flush()
                    else:
                        self.read_mess.ID = 0
                        for i in range(8):
                            self.read_mess.DATA[i] = 0
                    self.con.notify()
                    self.con.wait()
            else:
                result = self.PCAN.ReadFrame()
                if result[0] == PCAN_ERROR_OK:
                    self.read_mess = result[1]
                    msgID = hex(self.read_mess.ID)
                    msgData = []
                    for i in range(8):
                        msgData.append(hex(self.read_mess.DATA[i]))
                    self.fp.write('%s-----RECORD-----收到消息%s:%s\n' % (datetime.datetime.now(), msgID, msgData))
                    self.fp.flush()

    def SendCANmsgForResp(self, msg):
        with self.con:
            self.interrupt = True
            self.con.wait()
            self.PCAN.WriteFrame(msg)
            self.con.notify()

    def GetRespCANmsg(self, desCANmsgDict ,timeout, RemainFrames = 0):
        data = []
        timeGap = 0
        timeStart = time.time()
        isResponse = True
        while timeGap < timeout:
            with self.con:
                self.interrupt = True
                self.con.wait()
                if self.read_mess.ID == int(desCANmsgDict['ID'], 16):
                    lenth = len(desCANmsgDict['DATA'])
                    for i in range(lenth):
                        if desCANmsgDict['DATA'][i] == 'XX' or self.read_mess.DATA[i] == int(desCANmsgDict['DATA'][i], 16):
                            isResponse = True
                        else:
                            isResponse = False
                            break
                    if isResponse:
                        for i in range(8 - lenth):
                            data.append(hex(self.read_mess.DATA[i + lenth]))
                        # logger.info('CAN收到期望的消息%s:%s，请校验值%s' % (desCANmsgDict['ID'], desCANmsgDict['DATA'], data))
                        if self.read_mess.ID == int('719' ,16) and self.read_mess.DATA[0] == int('10' ,16):
                            num = 1
                            while((self.read_mess.DATA[1] - 6) > (num * 7)):
                                num = num + 1
                            stream_CANmsg = {'ID': '711', 'DATA': ['30', '00', '00', 'FF', 'FF', 'FF', 'FF', 'FF']}
                            streamResp_CANmsg = {'ID': '719', 'DATA': ['21']}
                            self.PCAN.WriteFrame(stream_CANmsg)
                            # logger.info('CAN消息为扩展帧，发送流控帧，还需要接收%s帧' % num)
                            self.con.notify()
                            for n in range(num):
                                # print('%s------%s------' %(datetime.datetime.now(), streamResp_CANmsg))
                                for d in self.GetRespCANmsg(streamResp_CANmsg, timeout, RemainFrames = (num - n - 1)):
                                    data.append(d)
                                streamResp_CANmsg['DATA'][0] = str(hex(int(streamResp_CANmsg['DATA'][0], 16) + 1))
                        if not RemainFrames:
                            self.interrupt = False
                        self.con.notify()
                        return data
                # logger.info('CAN没有收到期望的消息%s:%s' % (desCANmsgDict['ID'], desCANmsgDict['DATA']))
                timeGap = time.time() - timeStart
                self.con.notify()
        self.interrupt = False
        # self.con.notify()
        raise Exception('等待CAN消息%s超时' %desCANmsgDict)

    def StopRead(self):
        self.read_flag = False
        # time.sleep(1.1)
        # self.fp.close()

class WriteThread(threading.Thread):
    def __init__(self, pHandle, MsgDict, Period):
        threading.Thread.__init__(self)
        self.daemon = True
        self.PCAN = pHandle
        self.interrupt = False
        self.con = threading.Condition()
        self.msg = MsgDict
        self.per = Period
        self.thread_ID = MsgDict['ID']

    def run(self):
        self.PCAN.WriteFrame(self.msg)
        while self.per:
            time.sleep(self.per)
            self.PCAN.WriteFrame(self.msg)

    def stop(self):
        self.per = 0

class PCANHandle():
    def __init__(self):
        self.pcan = PCANDev()
        self.read_thread = ReadThread(self.pcan)
        self.read_thread.start()
        self.write_thread_pool = []
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Seed2Key_uniqe.dll")
        self.sa = windll.LoadLibrary(path)

    def SendCANmsg(self, MsgDict, Period = 0):
        logger.info('发送CAN消息,%s,周期:%s' % (MsgDict ,Period))
        if Period == 0:
            self.pcan.WriteFrame(MsgDict)
        elif len(self.write_thread_pool) == 0:
            new_thread = WriteThread(self.pcan, MsgDict, Period)
            new_thread.start()
            self.write_thread_pool.append(new_thread)
        else:
            has_sameID = False
            for write_thread in self.write_thread_pool:
                if MsgDict['ID'] == write_thread.thread_ID:
                    write_thread.msg = MsgDict
                    write_thread.per = Period
                    has_sameID = True
                    break
            if not has_sameID:
                new_thread = WriteThread(self.pcan, MsgDict, Period)
                new_thread.start()
                self.write_thread_pool.append(new_thread)

    def StopSendMsg(self, MsgID):
        logger.info('停止发送CAN消息,%s' % MsgID)
        if len(self.write_thread_pool) == 0:
            logger.info('没有CAN消息在发送')
        else:
            for i in range(len(self.write_thread_pool)):
                if MsgID == self.write_thread_pool[i].thread_ID:
                    self.write_thread_pool[i].stop()
                    self.write_thread_pool.pop(i)
                logger.info('%s的CAN消息已经停止发送' %MsgID)

    def StopAllSendMsg(self):
        if len(self.write_thread_pool) == 0:
            logger.info('没有CAN消息发送')
        else:
            #先模拟车辆熄火
            # self.SysPwdCtrl('off')
            logger.info('停止发送所有CAN消息')
            for write_thread in self.write_thread_pool:
                write_thread.stop()
            self.write_thread_pool = []

    def Stop(self):
        self.read_thread.StopRead()
        if len(self.write_thread_pool) > 0:
            self.StopAllSendMsg()
        time.sleep(1)
        self.pcan.close()

    def SendMsgForResp(self, sendMsg, respMsg, timeout = 5):
        logger.info('发送CAN消息，%s,' %sendMsg)
        # self.read_thread.SendCANmsgForResp(sendMsg)
        self.SendCANmsg(sendMsg)
        return self.read_thread.GetRespCANmsg(respMsg, timeout, RemainFrames = 0)

    def SendMsgForResp_ext(self, sendMsg, respMsg, timeout = 5):
        logger.info('发送CAN消息扩展帧，%s,' %sendMsg)
        msg = {'ID': '', 'DATA': ''}
        msg['ID'] = sendMsg['ID']
        msg['DATA'] = sendMsg['DATA'][0:8]
        data = self.SendMsgForResp(msg, DiagDict['streamRsp_CANMsg'])
        time2wait = (int(data[0], 16) + 1)/1000
        data_lst = sendMsg['DATA'][8:]
        DiagDict['stream_CANMsg']['DATA'][0] = '21'
        while (len(data_lst) > 0):
            for i in range(7):
                if len(data_lst) > 0:
                    DiagDict['stream_CANMsg']['DATA'][i + 1] = data_lst[0]
                    data_lst.pop(0)
                else:
                    DiagDict['stream_CANMsg']['DATA'][i + 1] = 'AA'
            time.sleep(time2wait)
            self.pcan.WriteFrame(DiagDict['stream_CANMsg'])
            num = int(DiagDict['stream_CANMsg']['DATA'][0], 16)
            if num == 47:
                num = 32
            else:
                num = num + 1
            numstr = hex(num)[2:]
            DiagDict['stream_CANMsg']['DATA'][0] = numstr
        return self.read_thread.GetRespCANmsg(respMsg, timeout, RemainFrames = 0)


    def WaitResp(self, respMsg, timeout = 5):
        return self.read_thread.GetRespCANmsg(respMsg, timeout, RemainFrames = 0)

    def Authenticate(self):
        #进入扩展模式
        reason = ''
        self.SendMsgForResp(DiagDict['keep_CANmsg'], DiagDict['keepRsp_CANmsg'])
        time.sleep(0.01)
        self.SendMsgForResp(DiagDict['ext_CANmsg'], DiagDict['extResp_CANmsg'])
        #尝试3次
        for i in range(3):
            try:
                seedList = self.SendMsgForResp(DiagDict['seed_CANmsg'], DiagDict['seedResp_CANmsg'])
                seedList.pop()
                for n in range(len(seedList)):
                    seedList[n] = seedList[n][2:]
                    if len(seedList[n]) == 1:
                        seedList[n] = '0' + seedList[n]
                seedStr = ''.join(seedList)
                # print(int(seedStr, 16))
                seedCalc = c_ulong(int(seedStr, 16))
                self.sa.Seed2Key.restype = c_ulong
                keyRst = self.sa.Seed2Key(seedCalc, c_int(1))
                # print(keyRst, hex(keyRst))
                keyStr = str((hex(keyRst)))[2:]
                lenth = len(keyStr)
                for i in range(4):
                    if (lenth - (2 * i)) > 0:
                        DiagDict['key_CANmsg']['DATA'][6 - i] = keyStr[-(2 * (i + 1)):(lenth - (2 * i))]
                    else:
                        DiagDict['key_CANmsg']['DATA'][6 - i] = '00'
                rstData = self.SendMsgForResp(DiagDict['key_CANmsg'], DiagDict['keyResp_CANmsg'])
                if len(rstData) > 0:
                    return (True, '')
                else:
                    logger.info('诊断CAN鉴权失败')
            except Exception as e:
                logger.info('诊断CAN鉴权失败:%s' %e)
                reason = str(e)
        return (False, reason)


    def WriteDiagCfgInApp(self, diagMsgDictList):
        try:
            # 通过鉴权
            authRst = self.Authenticate()
            if authRst[0]:
                for diagMsgDict in diagMsgDictList:
                     #写入C106
                    if diagMsgDict['ID'] == 'C106':
                        for i in range(3):
                            DiagDict['wC106_CANmsg']['DATA'][4+i] = diagMsgDict['DATA'][i]
                        self.SendMsgForResp(DiagDict['wC106_CANmsg'], DiagDict['wC106Resp_CANmsg'])
                    #写入C001
                    if diagMsgDict['ID'] == 'C001':
                        for i in range(64):
                            DiagDict['wC001_CANmsg']['DATA'][5 + i] = diagMsgDict['DATA'][i]
                        self.SendMsgForResp(DiagDict['keep_CANmsg'], DiagDict['keepRsp_CANmsg'])
                        time.sleep(0.01)
                        self.SendMsgForResp_ext(DiagDict['wC001_CANmsg'], DiagDict['wC001Resp_CANmsg'])
                    #写入C004
                    if diagMsgDict['ID'] == 'C004':
                        for i in range(64):
                            DiagDict['wC004_CANmsg']['DATA'][5 + i] = diagMsgDict['DATA'][i]
                        self.SendMsgForResp(DiagDict['keep_CANmsg'], DiagDict['keepRsp_CANmsg'])
                        time.sleep(0.01)
                        self.SendMsgForResp_ext(DiagDict['wC004_CANmsg'], DiagDict['wC004Resp_CANmsg'])
                return(True, '')
            else:
                return(False, authRst[1])
        except Exception as e:
            logger.info('APP模式写入DID失败:%s' %e)
            return(False, str(e))

    def WriteDiagCfgInEol(self, diagMsgDictList):
        try:
            # 通过鉴权
            authRst = self.Authenticate()
            if authRst[0]:
                # 进入EOL
                self.SendMsgForResp(DiagDict['eolin1_CANmsg'], DiagDict['eolin1Resp_CANmsg'])
                self.SendMsgForResp(DiagDict['eolin2_CANmsg'], DiagDict['eolin2Resp_CANmsg'])
                self.SendCANmsg(DiagDict['reset_CANmsg'])
                time.sleep(5)
                for diagMsgDict in diagMsgDictList:
                    #写入B210
                    if diagMsgDict['ID'] == 'B210':
                        for i in range(2):
                            DiagDict['wB210_CANmsg']['DATA'][4+i] = diagMsgDict['DATA'][i]
                            DiagDict['wB210bak_CANmsg']['DATA'][4 + i] = diagMsgDict['DATA'][i]
                        self.SendMsgForResp(DiagDict['wB210_CANmsg'], DiagDict['wB210Resp_CANmsg'])
                        self.SendMsgForResp(DiagDict['wB210bak_CANmsg'], DiagDict['wB210bakResp_CANmsg'])
                    # 写入B200
                    elif diagMsgDict['ID'] == 'B200':
                        for i in range(2):
                            DiagDict['wB200_CANmsg']['DATA'][4 + i] = diagMsgDict['DATA'][i]
                            DiagDict['wB200bak_CANmsg']['DATA'][4 + i] = diagMsgDict['DATA'][i]
                        self.SendMsgForResp(DiagDict['wB200_CANmsg'], DiagDict['wB200Resp_CANmsg'])
                        self.SendMsgForResp(DiagDict['wB200bak_CANmsg'], DiagDict['wB200bakResp_CANmsg'])
                #退出EOL
                self.SendMsgForResp(DiagDict['eolout1_CANmsg'], DiagDict['eolout1Resp_CANmsg'])
                self.SendMsgForResp(DiagDict['eolout2_CANmsg'], DiagDict['eolout2Resp_CANmsg'])
                return (True, '')
            else:
                return(False, authRst[1])
        except Exception as e:
            logger.info('EOL模式写入DID失败:%s' % e)
            return (False, str(e))

    def ReadDiagConfig(self, diagMsgDict):
        readRst = False
        if diagMsgDict['ID'] == 'C106':
            try:
                dataRst = self.SendMsgForResp(DiagDict['rC106_CANmsg'], DiagDict['rC106Resp_CANmsg'])
                for i in range(len(diagMsgDict['DATA'])):
                    if int(diagMsgDict['DATA'][i], 16) == int(dataRst[i], 16):
                        readRst = True
                    else:
                        readRst = False
                        break
                if readRst:
                    return(True, '')
                else:
                    return (False, 'DataNotCompare')
            except Exception as e:
                logger.info('C106读取失败:%s' %e)
                return(False, str(e))

    def InitDiagConfig(self):
        try:
        #通过鉴权
            authRst = self.Authenticate()
            if authRst[0]:
                #进入EOL将EE恢复初始化并退出EOL
                self.SendMsgForResp(DiagDict['eolin1_CANmsg'], DiagDict['eolin1Resp_CANmsg'])
                self.SendMsgForResp(DiagDict['eolin2_CANmsg'], DiagDict['eolin2Resp_CANmsg'])
                self.SendCANmsg(DiagDict['reset_CANmsg'])
                time.sleep(10)
                self.SendMsgForResp(DiagDict['initee_CANmsg'], DiagDict['initeeResp_CANmsg'])
                self.SendMsgForResp(DiagDict['eolout1_CANmsg'], DiagDict['eolout1Resp_CANmsg'])
                self.SendMsgForResp(DiagDict['eolout2_CANmsg'], DiagDict['eolout2Resp_CANmsg'])
                return(True, '')
            else:
                return(False, authRst[1])
        except Exception as e:
            logger.info('EE恢复初始化失败:%s' %e)
            return(False, str(e))

    def SysPwdCtrl(self, mode):
        if mode == 'on':
            self.SendCANmsg(DiagDict['pwrmd_CANmsg'], 0.01)
            time.sleep(0.5)
            DiagDict['pwrmd_CANmsg']['DATA'][0] = '0E'
            self.SendCANmsg(DiagDict['pwrmd_CANmsg'], 0.01)
            time.sleep(0.02)
            DiagDict['pwrmd_CANmsg']['DATA'][0] = '0B'
            self.SendCANmsg(DiagDict['pwrmd_CANmsg'], 0.01)
            time.sleep(1)
            DiagDict['pwrmd_CANmsg']['DATA'][0] = '0A'
            self.SendCANmsg(DiagDict['pwrmd_CANmsg'], 0.01)
            time.sleep(0.03)
            DiagDict['pwrmd_CANmsg']['DATA'][0] = '0E'
            self.SendCANmsg(DiagDict['pwrmd_CANmsg'], 0.01)
        elif mode == 'off':
            DiagDict['pwrmd_CANmsg']['DATA'][0] = '0E'
            self.SendCANmsg(DiagDict['pwrmd_CANmsg'], 0.01)
            time.sleep(0.5)
            DiagDict['pwrmd_CANmsg']['DATA'][0] = '05'
            self.SendCANmsg(DiagDict['pwrmd_CANmsg'], 0.01)
            time.sleep(0.02)
            DiagDict['pwrmd_CANmsg']['DATA'][0] = '00'
            self.SendCANmsg(DiagDict['pwrmd_CANmsg'], 0.01)
        else:
            logger.info('车辆点火控制参数错误')



if __name__ == '__main__':
    can_api = PCANHandle()
    can_api.Authenticate()