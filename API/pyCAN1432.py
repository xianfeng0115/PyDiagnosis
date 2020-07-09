#!/usr/bin/env python
# -*- coding:utf-8 -*-

from API.globalpkg.PCANDev import *
from API.globalpkg.diagcandbc import *
from binascii import unhexlify
from concurrent.futures import ThreadPoolExecutor
logger = None
import Common.CommonVar
from Common.CommonFun import *
from API.Logger import Loggers
import asyncio
import queue
from threading import Thread,Event
import win32event
from func_timeout import func_set_timeout
if not Common.CommonVar.logger:
    log = Loggers(filename='AutoTest.log', log_dir='.', logtype='console')
    Common.CommonVar.logger = log.logger
    logger = log.logger

FRAME_WIDTH = 760
FRAME_HEIGHT = 650
GROUPBOX_WIDTH = 745
GROUPBOX_HEIGHT = 70
ENABLE_CAN_FD = True
TIMEOUT = 10

class CANAPI(PCANBasic):
    """
    CAN總綫
    """
    def __init__(self):
        PCANBasic.__init__(self)
        self.baudrate = PCAN_BAUD_500K
        self.m_PcanHandle = PCAN_USBBUS1
        self.read_mess = TPCANMsg()
        self.init()
        self.msg_que = queue.Queue()
        self.send_que = queue.Queue()
        self.REV_FLAG = 1
        self.SEND_FLAG = 1
        self._endEvent = Event()
        self._revEvent = Event()
        self._sendEvent = Event()
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.rev_mornitor()
        self.send_mornitor()




    def init(self):
        try:
            result = self.Initialize(self.m_PcanHandle, self.baudrate)
            if result ==0:
                pass
            if result != PCAN_ERROR_OK:
                if result != PCAN_ERROR_CAUTION:
                    raise Exception('Error!', self.GetFormatedError(result))
            self.m_ReceiveEvent = win32event.CreateEvent(None, 0, 0, None)
            setResult = self.SetValue(self.m_PcanHandle, PCAN_RECEIVE_EVENT, self.m_ReceiveEvent)
            if setResult != PCAN_ERROR_OK:
                raise Exception('Error!', self.GetFormatedError(setResult))
        except Exception as e:
            logger.info('PCAN init failed:%s' %e)

    def get_can_msg(self,id, data):
        msg = {}
        msg['ID'] = id
        msg['DATA'] = []
        for i in range(0,len(data),2):
            msg['DATA'].append(data[i:i+2])
        return msg


    def GetFormatedError(self, error):
        stsReturn = self.GetErrorText(error, 0)
        if stsReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            return stsReturn[1]

    def sendMsg(self):
        while self.SEND_FLAG:
            if not self.msg_que.empty() and not self._sendEvent.isSet():
                data = self.msg_que.get()
                self.pool.submit(self.handle_msg, data)

    def handle_msg(self, data):
        msgDict = self.cmd_map(data)
        self.WriteFrame(msgDict)

    def cmd_map(self, data):

        return data

    @time_out
    @func_set_timeout(TIMEOUT)
    def revMsg(self,id='719'):
        try:
            self._revEvent.wait()
            result = self.msg_que.get()
            if result.get('ID') != id:
                self.msg_que.put(result)
                return self.revMsg(id)

            return result
        except Exception as e:
            pass


    def Timing_send(self, msg,timing):
        try:
            self.timing_send = Thread(target=self.TimingMsg, args=(msg,timing))
            self.timing_send.daemon = True
            self.timing_send.start()
        except Exception as e:
            logger.info('send_mornitor error:%s'%e)

    def TimingMsg(self,msg,timing):
        while 1:
            self.WriteFrame(msg)
            time.sleep(timing)

    def WriteFrame(self, MsgDict):
        CANMsg = TPCANMsg()
        CANMsg.ID = int(MsgDict['ID'], 16)
        CANMsg.LEN = 8
        CANMsg.MSGTYPE = PCAN_MESSAGE_STANDARD
        if len(MsgDict['DATA']) < 8 :
            logger.info('发送消息%s:%s' % (MsgDict['ID'], MsgDict['DATA']))
        for i in range(8):
            CANMsg.DATA[i] = int(MsgDict['DATA'][i], 16)
        # logger.info('发送消息%s:%s' % (MsgDict['ID'], MsgDict['DATA']))
        send_rst = self.Write(self.m_PcanHandle, CANMsg)
        # if CANMsg.ID == int('711', 16) or CANMsg.ID == int('6E1', 16):
        #     time.sleep(0.001)
        if send_rst != PCAN_ERROR_OK:
            logger.info(self.GetFormatedError(send_rst))
        else:
            pass
            #logger.info('send :%s success!'%str(MsgDict))




    def close(self):
        releaseRst = self.Uninitializsuccesse(self.m_PcanHandle)
        self.REV_FLAG = False
        self.rev_mornitor_wait()
        if releaseRst == PCAN_ERROR_OK:
            logger.info("PCAN was successfully released")
        else:
            logger.info(self.GetFormatedError(releaseRst))

    def btnRelease_Click(self):
        # if WINDOWS_EVENT_SUPPORT:
        #     if self.m_ReadThread != None:
        #         self.m_Terminated = True
        #         self.m_ReadThread.join()
        #         self.m_ReadThread = None

        # We stop to read from the CAN queue
        #
        #self.tmrRead.stop()

        # Releases a current connected PCAN-Basic channel
        #
        self.Uninitialize(self.m_PcanHandle)

        # Sets the connection status of the main-form
        #
    def rev_mornitor(self):
        try:
            self.rev_t = Thread(target=self.ReadFrame,)
            self.rev_t.daemon = True
            self.rev_t.start()
        except Exception as e:
            logger.info('rev_mornitor error:%s'%e)

    def send_mornitor(self):
        try:
            self._sendEvent.clear()
            self.send_t = Thread(target=self.sendMsg,)
            self.send_t.daemon = True
            self.send_t.start()
        except Exception as e:
            logger.info('send_mornitor error:%s'%e)

    def rev_mornitor_wait(self):
        self._endEvent.wait()


    def ReadFrame(self):
        # We execute the "Read" function of the PCANBasic
        #
        try:
            while self.REV_FLAG:
                result = self.Read(self.m_PcanHandle)
                resultlist = []
                if result[0] == 0:
                    try:
                        for i in range(8):
                            resultlist.append(hex(result[1].DATA[i])[2:].zfill(2).upper())
                        msg = {}
                        msg['ID'] = hex(result[1].ID)[2:]
                        msg['DATA'] = resultlist
                        if msg['ID'] in ['40a','34d']:
                            continue
                        # logger.info('ReadFrame:%s' %str(msg))
                        self.msg_que.put(msg)

                    except Exception as e:

                        logger.info('ReadFrame-if:%s' % e)
                        self.msg_que.put(resultlist)
                        self._revEvent.set()

                    finally:
                        time.sleep(0.01)
                        self._revEvent.set()
                elif result[0] == 32:
                    continue

                else:
                    try:
                        self.msg_que.put(resultlist)
                    except Exception as e:
                        logger.info('ReadFrame-else:%s'%e)
                        self.msg_que.put(resultlist)
                        self._revEvent.set()
                    finally:
                        time.sleep(0.01)
                        self._revEvent.set()
        except Exception as e:
            logger.info('ReadFrame error:%s'%e)
        finally:
            self._endEvent.set()

    def SendMsgForResp(self, MsgDict):
        try:
            logger.info('send:%s' % MsgDict)
            self._sendEvent.set()
            self.WriteFrame(MsgDict)
            result = self.revMsg()
            self._sendEvent.clear()
            logger.info('rev:%s' % result)
        except Exception as e:
            logger.info('SendMsgForResp:%s' % e)
            result = None
        return result

    def hanld_flow_msg(self, msg):
        first_msg = []
        #增加多针的标识
        first_msg.append('10')
        msglist = msg.get('DATA')
        id = msg.get('ID')
        #增加多帧的长度
        msg_len = len(msglist)
        need_len = 7- ((msg_len-6)%7)
        first_msg.append(hex(msg_len).strip('0x').upper().zfill(2))
        first_msg += msglist[:6]
        first_dict = {'ID': id, 'DATA': first_msg}
        resultdict = self.SendMsgForResp(first_dict)
        result = resultdict.get('DATA')
        if result[0] == '30' or result[0] == '0A':
            childlist = msglist[6:]
            index = 21
            for child in range(0, len(childlist),7):
                nextlist = childlist[child:child+7]
                if len(nextlist) < 7:
                    nextlist = [str(index)] + nextlist + ['FF']*(7-len(nextlist))
                    enddict = {'ID': id, 'DATA': nextlist}
                    result = self.SendMsgForResp(enddict)
                    return result
                else:
                    nextdict = {'ID': id, 'DATA': [str(index)] + nextlist}
                    self.WriteFrame(nextdict)
                    index += 1
                    time.sleep(0.03)
        else:
            return []
            logger.info('send flow msg error')

    def send_flow_msg(self,id , msg):
        MsgDict = self.get_can_msg(id,msg)
        if len(msg) <= 16:
            result = self.SendMsgForResp(MsgDict)
        else:
            result = self.hanld_flow_msg(MsgDict)
        return result




if __name__ == '__main__':
    can_api = CANAPI()
    """FF FF FF FF 34 36 30 30 30 30 
31 38 31 30 39 32 38 35 36 38 36 FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF 01
"""
    MsgDict = {'ID':'711', 'DATA':['10', '28', '2E', 'CA', '02', 'FF', 'FF', 'FF','FF','34', '36', '30','30', '30',
                                   '30','31', '38', '31', '30', '39' ,'32', '38','23', '35', '36', '38', '36','00',
                                   'FF', 'FF']}

    result = can_api.SendMsgForResp(MsgDict)
    print(result)
    can_api.btnRelease_Click()