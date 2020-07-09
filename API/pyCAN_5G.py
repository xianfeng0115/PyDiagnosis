#!/usr/bin/env python
# -*- coding:utf-8 -*-

from API.globalpkg.PCANDev import *
from tornado import ioloop, gen, iostream
from API.globalpkg.diagcandbc import *
from binascii import unhexlify
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from collections import deque
import Common.CommonVar
from Common.CommonFun import *
from Common.CommonVar import logger
from Communication.websocket import *
from datetime import datetime
import asyncio
from queue import *
try:
    from DB.Can_table import *
except:
    pass
from threading import Thread, Event
import win32event
import pandas as pd
from func_timeout import func_set_timeout
from ResponseMap.Can_Map import *
from copy import deepcopy
from API.Py_excle import *

FRAME_WIDTH = 760
FRAME_HEIGHT = 650
GROUPBOX_WIDTH = 745
GROUPBOX_HEIGHT = 70
ENABLE_CAN_FD = True
TIMEOUT = 3


class Executor(ThreadPoolExecutor):
    """ 创建多线程的线程池，线程池的大小为10
    创建多线程时使用了单例模式，如果Executor的_instance实例已经被创建，
    则不再创建，单例模式的好处在此不做讲解
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=2000)
        return cls._instance


class CANAPI_5G(PCANBasic):
    """
    CAN總綫
    """
    executor = Executor()

    def __init__(self):
        self.enable = True
        #rootpath = os.environ['root_path']
        rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logpath = os.path.join(rootpath, 'Log')
        cfg = pyExcel.get_instances()
        self.logger = Loggers.get_instances(filename='bcm.log', log_dir=logpath,
                                            logtype=cfg.get_cfgkey_value('bcm_logtype'))
        PCANBasic.__init__(self)
        path = os.path.join(rootpath, 'API', "globalpkg", "Seed2Key_uniqe.dll")
        self.sa = windll.LoadLibrary(path)

        self.ext_CANmsg = {'ID': '714', 'DATA': ['02', '10', '03', '00', '00', '00', '00', '00']}
        self.seed_CANmsg = {'ID': '714', 'DATA': ['02', '27', '01', '00', '00', '00', '00', '00']}

        self.responseFlag = 0
        self.baudrate = PCAN_BAUD_500K
        self.m_PcanHandle = PCAN_USBBUS1
        self.thread_pool = ThreadPoolExecutor(10)
        self.rev_list = []
        self.read_mess = TPCANMsg()
        self.init()
        self.setDict = {}
        self.msg_que = Queue()
        self.response_que = Queue()
        self.cmsg_que = Queue()
        self.vue_que = deque()
        self.REV_FLAG = 1
        self.SEND_FLAG = 1
        self._endEvent = Event()
        self._revEvent = Event()
        self._sendEvent = Event()
        self.rev_lock = threading.Lock()
        self.writeEvent = threading.Lock()
        self.sendEvent = threading.Lock()
        self.db_lock = threading.Lock()

        self.websocket = WebSocketSever
        self.r_mornitor()
        self.w_mornitor()
        self.c_mornitor()
        pass

    def r_mornitor(self):
        # yield self.rev_mornitor()
        self.thread_pool.submit(self.ReadFrame)
    #
    # def v_mornitor(self):
    #     # yield self.rev_mornitor()
    #     self.thread_pool.submit(self.send_vue)

    def w_mornitor(self):
        # tornado.ioloop.IOLoop.instance().spawn_callback(self.send_mornitor)
        # self.send_mornitor()
        self.thread_pool.submit(self.send_mornitor)

    def c_mornitor(self):
        self.thread_pool.submit(self.send_cmornitor)

    def init(self):
        try:
            result = self.Initialize(self.m_PcanHandle, self.baudrate)
            if result == 0:
                pass
            if result != PCAN_ERROR_OK:
                if result != PCAN_ERROR_CAUTION:
                    raise Exception('Error!', self.GetFormatedError(result))
            self.m_ReceiveEvent = win32event.CreateEvent(None, 0, 0, None)
            setResult = self.SetValue(self.m_PcanHandle, PCAN_RECEIVE_EVENT, self.m_ReceiveEvent)
            if setResult != PCAN_ERROR_OK:
                raise Exception('Error!', self.GetFormatedError(setResult))
        except Exception as e:
            self.logger.info('PCAN init failed:%s' % e)

    def get_can_msg(self, id, data):
        msg = {}
        msg['ID'] = id
        msg['DATA'] = []
        for i in range(0, len(data), 2):
            msg['DATA'].append(data[i:i + 2])
        return msg

    def GetFormatedError(self, error):
        stsReturn = self.GetErrorText(error, 0)
        if stsReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            return stsReturn[1]

    @gen.coroutine
    def sendMsg(self):
        while self.enable:
            data = self.msg_que.get()
            if data:
                self.logger.info('sendMsg moniter rev:%s' % data)
                try:
                    self.handle_msg(data)
                except Exception as e:
                    self.logger.info('sendMsg error:%s' % e)
                # finally:
                #     self.msg_que.task_done()

    def handle_msg(self, data):
        msgDict = self.cmd_map(data)
        if msgDict:
            self.WriteFrame(msgDict)

    def cmd_map(self, data):

        return data

    @time_out
    @func_set_timeout(TIMEOUT)
    def revMsg(self, id='71c'):
        try:
            while True:
                result = self.response_que.get()

                if type(result) is dict and result.get('ID') == id:
                    break
                self.msg_que.put(result)
            return result
        except Exception as e:
            return result

    @time_out
    @func_set_timeout(100)
    def revmanyMsg(self, sorceid, id='71c'):
        result_list = []
        sumlen = 0
        msglen = 1
        try:

            while True:
                if sumlen >= msglen:
                    break
                result = self.rev_res_que()
                print(result)
                if result and type(result) is dict and result.get('ID') == id:
                    if result.get('DATA')[0] == '10':
                        msglen = int(result.get('DATA')[1], 16)
                        sumlen = 6
                        nextMsg = {'ID': sorceid, 'DATA': ['30', '00', '00', '00', '00', '00', '00', '00']}
                        self.WriteFrame(nextMsg, display=False)
                    elif result.get('DATA')[0:4] == ['03', '7F', '22', '78']:
                       pass
                    else:
                        sumlen += 7
                    result_list.append(result)

                else:
                    self.msg_que.put(result)
                time.sleep(0.1)
            return result_list
        except Exception as e:
            return result_list

    @time_out
    @func_set_timeout(TIMEOUT)
    def rev_res_que(self):
        result = None
        while 1:
            if not self.response_que.empty():
                result = self.response_que.get()
                break
        return result

    def Timing_send_can(self, msg, timing, count=-1, Intervaltime=0, delaytime=0, display=1):
        try:
            # self.timing_send = Thread(target=self.TimingMsg, args=(msg,timing))
            # self.timing_send.daemon = True
            # self.timing_send.start()
            # yield self.TimingMsgCan(msg,timing,count,Intervaltime,delaytime)
            self.thread_pool.submit(self.TimingMsgCan, msg, timing, count, Intervaltime, delaytime, display)
        except Exception as e:
            self.logger.info('Timing_send error:%s' % e)

    def Timing_send_API(self, msgname, timing, count=-1, Intervaltime=0, delaytime=0, display=1):
        try:
            # self.timing_send = Thread(target=self.TimingMsg, args=(msg,timing))
            # self.timing_send.daemon = True
            # self.timing_send.start()
            # yield self.TimingMsgCan(msg,timing,count,Intervaltime,delaytime)
            self.thread_pool.submit(self.TimingMsgCanAPI, msgname, timing, count, Intervaltime, delaytime, display)
        except Exception as e:
            self.logger.info('Timing_send error:%s' % e)

    def TimingMsgCanAPI(self, msgname, timing, count=-1, Intervaltime=0, delaytime=0, display=1):

        if count != -1:
            while count:
                msg = getattr(self, msgname)
                if not self.enable:
                    break
                time.sleep(delaytime)
                timedata = Intervaltime if Intervaltime else delaytime
                self.WriteFrame(msg, timedata)
                time.sleep(Intervaltime)
                count -= 1
        else:
            i = 1
            while self.enable:
                msg = getattr(self, msgname)
                if i == display:
                    self.WriteFrame(msg, timing, display=True)
                    i = 1
                else:
                    self.WriteFrame(msg, timing, display=False)
                i += 1
                time.sleep(timing)
        self.Timing_after()

    def TimingMsgCan(self, msg, timing, count=-1, Intervaltime=0, delaytime=0, display=1):

        if count != -1:
            while count:
                if not self.enable:
                    break
                time.sleep(delaytime)
                timedata = Intervaltime if Intervaltime else delaytime
                self.WriteFrame(msg, timedata)
                time.sleep(Intervaltime)
                count -= 1
        else:
            i = 1
            while self.enable:
                if i == display:
                    self.WriteFrame(msg, timing, display=True)
                    i = 1
                else:
                    self.WriteFrame(msg, timing, display=False)
                i += 1
                time.sleep(timing)
        self.Timing_after()

    def Timing_after(self):
        pass

    def WriteFrame(self, MsgDict, cycle=None, display=True):
        CANMsg = TPCANMsg()
        CANMsg.ID = int(MsgDict['ID'], 16)
        CANMsg.LEN = 8
        CANMsg.MSGTYPE = PCAN_MESSAGE_STANDARD
        msg_data = []
        if type(MsgDict['DATA']) is not list:
            msg_data = [MsgDict['DATA'][i:i + 2] for i in range(0, len(MsgDict['DATA']), 2)]
        else:
            msg_data = MsgDict['DATA']
        for i in range(8):
            CANMsg.DATA[i] = int(msg_data[i], 16)
        if MsgDict['ID'] == '714':
            self.logger.info('发送消息%s:%s' % (MsgDict['ID'], ''.join(msg_data)))
        send_rst = self.Write(self.m_PcanHandle, CANMsg)

        if display:
            self.send_vue_msg(MsgDict, 'TX')

        if send_rst != PCAN_ERROR_OK:
            self.logger.info(self.GetFormatedError(send_rst))
        else:
            pass
            # self.logger.info('send :%s success!'%str(MsgDict))

    def insert_db(self, MsgDict, cycle='-', msgMode='Tx'):
        try:
            self.db_lock.acquire()
            db_session = Common.CommonVar.Session()
            result = db_session.query(CanTask).filter(
                and_(CanTask.content == str(MsgDict['DATA']), CanTask.can_id == MsgDict['ID'])).first()
            if not result:

                can_task = CanTask(content=str(MsgDict['DATA']), can_len=len(MsgDict['DATA']),
                                   can_id=MsgDict['ID'], Tx_Rx=msgMode, cycle_time=str(cycle), explain='')
                db_session.add(can_task)
                db_session.commit()
            else:
                result.current = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                db_session.commit()
            self.db_lock.release()
            return result
        except Exception as e:
            pass

    def insert_all_avn(self, table_name, data_dict):
        df = pd.DataFrame(data_dict)
        df.to_sql(table_name, con=Common.CommonVar.ENGINE, if_exists='append', index=False)

    def close(self, webname=None):

        self.REV_FLAG = False
        self.SEND_FLAG = False
        self.enable = 0
        if webname:
            self.websocket.webname = webname
        releaseRst = self.btnRelease_Click()
        pass

    def btnRelease_Click(self):
        # if WINDOWS_EVENT_SUPPORT:
        #     if self.m_ReadThread != None:
        #         self.m_Terminated = True
        #         self.m_ReadThread.join()
        #         self.m_ReadThread = None

        # We stop to read from the CAN queue
        #
        # self.tmrRead.stop()

        # Releases a current connected PCAN-Basic channel
        #
        self.Uninitialize(self.m_PcanHandle)

        # Sets the connection status of the main-form
        #

    @gen.coroutine
    def rev_mornitor(self):
        try:
            # self.rev_t = Thread(target=self.ReadFrame,)
            # self.rev_t.daemon = True
            # self.rev_t.start()
            while 1:
                yield self.ReadFrame()
        except Exception as e:
            self.logger.info('rev_mornitor error:%s' % e)

    def send_vue(self):

        while self.SEND_FLAG:

            MsgDict, Modle = self.vue_que.popleft()

            current = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            cycle_time = '-' if 'cycle_time' not in MsgDict else MsgDict['cycle_time']
            childlist = []
            content = MsgDict.get('DATA')
            if type(MsgDict.get('DATA')) is str:
                content = [MsgDict.get('DATA')[i:i + 2] for i in range(0, len(MsgDict.get('DATA')), 2)]
            lendata = len(MsgDict.get('DATA'))
            content = ' '.join(content)

            showid = {
                'Tx_Rx': Modle,
                'can_id': MsgDict['ID'],
                'content': content,
                'cycle_time': cycle_time,
                'can_len': lendata,
                'current': current,
            }
            self.websocket.send_message(showid, 'bcm')
            time.sleep(0.001)

    def send_vue_msg(self, MsgDict, Modle):

        current = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        cycle_time = '-' if 'cycle_time' not in MsgDict else MsgDict['cycle_time']
        childlist = []
        content = MsgDict.get('DATA')
        if type(MsgDict.get('DATA')) is str:
            content = [MsgDict.get('DATA')[i:i + 2] for i in range(0, len(MsgDict.get('DATA')), 2)]
        lendata = len(MsgDict.get('DATA'))
        content = ' '.join(content)

        showid = {
            'Tx_Rx': Modle,
            'can_id': MsgDict['ID'],
            'content': content,
            'cycle_time': cycle_time,
            'can_len': lendata,
            'current': current,
        }
        self.sendEvent.acquire()
        self.websocket.send_message(showid, 'bcm')
        self.sendEvent.release()

    def send_mornitor(self):
        try:
            while self.SEND_FLAG:

                data = self.msg_que.get(False)
                if data:
                    # try:
                    if self.websocket:
                        self.send_vue_msg(data, 'RX')
                        self.cmd_map(data, self.insert_db)


                    # except Exception as e:
                    #     raise
                    #     self.logger.info('sendMsg error:%s' % e)
                    # finally:
                    #     self.msg_que.task_done()
        except Exception as e:
            pass

    def send_cmornitor(self):
        try:
            while self.SEND_FLAG:
                try:
                    data = self.cmsg_que.get(False)
                    if data:
                        self.send_vue_msg(data, 'RX')
                        # MsgDict = data
                        # lendata = len(MsgDict['DATA']) if type(MsgDict['DATA']) is list else len(MsgDict['DATA']) / 2
                        # current = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        # cycle_time = '-' if 'cycle_time' not in MsgDict else MsgDict['cycle_time']
                        #
                        # showid = {
                        #     'Tx_Rx': 'Rx',
                        #     'can_id': MsgDict['ID'],
                        #     'content': MsgDict['DATA'],
                        #     'cycle_time': cycle_time,
                        #     'can_len': lendata,
                        #     'current': current,
                        # }
                        # result = self.websocket.send_message(showid)
                except Exception as e:
                    self.logger.info('sendMsg error:%s' % e)
                finally:
                    self.cmsg_que.task_done()
                time.sleep(0.01)
        except:
            pass

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

                        for i in range(result[1].DATA._length_):
                            resultlist.append(hex(result[1].DATA[i])[2:].zfill(2).upper())
                        msg = {}
                        msg['ID'] = hex(result[1].ID)[2:]
                        msg['DATA'] = resultlist

                        # self.logger.info('接收消息%s:%s' % (msg.get('ID'), ''.join(msg.get('DATA'))))
                        if resultlist[0] == '10':
                            newmsg = {}
                            newmsg['ID'] = '714'
                            newmsg['DATA'] = ['30', '00', '00', '00', '00', '00', '00', '00']
                            self.WriteFrame(newmsg, display=False)

                        if not msg['ID'] in ['3e9', '472','451','1fb','3d5','41f','1f1']:
                            self.logger.info('接收消息%s:%s' % (msg.get('ID'), ''.join(msg.get('DATA'))))
                            # self.logger.info('ReadFrame:%s' % str(msg))
                            # self.cmd_map(msg,self.insert_db)
                            self.msg_que.put(msg)
                            if self.responseFlag:
                                self.response_que.put(msg)
                        else:
                            self.cmsg_que.put(msg)


                        # if msg['ID'] in []:
                        #     self.quick_response(msg)
                        # else:
                        #
                        #     self.msg_que.put(msg)

                    except Exception as e:

                        self.logger.info('ReadFrame-if:%s' % e)
                        self.msg_que.put(resultlist)
                        # self._revEvent.set()

                        # self._revEvent.set()
                elif result[0] == 32:
                    pass

                else:
                    try:
                        self.logger.info('ReadFrame-else:%s' % str(resultlist))
                    except Exception as e:
                        self.logger.info('ReadFrame-else:%s' % e)
                        # self._revEvent.set()

        except Exception as e:
            self.logger.info('ReadFrame error:%s' % e)
        # finally:
        #     # self._endEvent.set()
        #     pass

    def quick_response(self, msg):
        pass

    def handle_app_msg(self, msg):

        pass

    def SendMsgForResp(self, MsgDict, id, open_que = False):
        try:
            self.responseFlag = 1
            self.WriteFrame(MsgDict, display=False)
            result = self.revMsg(id)
            if not open_que:
                self.responseFlag = 0
                self.response_que.queue.clear()
            return result
        except Exception as e:
            self.logger.info('SendMsgForResp:%s' % e)
            return result

    def get_hand_msg(self, index, pre_hand):
        if index == 1:
            hand_msg = '10'
        elif index == 2:
            hand_msg = '21'
        else:
            hand_msg = str(int(pre_hand) + 1)
        return hand_msg

    def SendMsgFormanyResp(self, MsgDict, id):
        try:
            self.responseFlag = 1
            if len(MsgDict.get('DATA'))>8:
                index = 0
                sendmsg = {}
                sendmsg['ID'] = MsgDict.get('ID')
                sendmsg['DATA'] = []

                pre_hand = ''
                for i in range(0, len(MsgDict.get('DATA')), 7):
                    time.sleep(0.01)
                    index += 1
                    hand_msg = self.get_hand_msg(index, pre_hand)
                    pre_hand = hand_msg
                    if index == 1:
                        sendmsg['DATA'] = [hand_msg] + MsgDict.get('DATA')[i:i+7]
                        print(sendmsg)

                        response_first = self.SendMsgForResp(sendmsg, id, open_que=True)
                        if response_first.get('DATA')[0] != '30':
                            raise
                    elif i+7 > len(MsgDict.get('DATA')):
                        cha = (i+7) - len(MsgDict.get('DATA'))
                        sendmsg['DATA'] = [hand_msg] + MsgDict.get('DATA')[i:len(MsgDict.get('DATA'))] + cha*['FF']
                        result = self.SendMsgForResp(sendmsg, id)

                    elif i+7 == len(MsgDict.get('DATA')):
                        sendmsg['DATA'] = [hand_msg] + MsgDict.get('DATA')[i:i+7]
                        result = self.SendMsgForResp(sendmsg, id)
                    else:
                        sendmsg['DATA'] = [hand_msg] + MsgDict.get('DATA')[i:i+7]
                        self.WriteFrame(sendmsg, display=False)

            else:
                self.WriteFrame(MsgDict, display=False)
                result = self.revmanyMsg(MsgDict.get('ID'), id)
            return result
        except Exception as e:
            self.logger.info('SendMsgForResp:%s' % e)
            return result

    def hanld_flow_msg(self, msg, dstcanid):
        first_msg = []
        # 增加多针的标识
        first_msg.append('10')
        msglist = msg.get('DATA')
        id = msg.get('ID')
        # 增加多帧的长度
        msg_len = len(msglist)
        need_len = 7 - ((msg_len - 6) % 7)
        first_msg.append(hex(msg_len).strip('0x').upper().zfill(2))
        first_msg += msglist[:6]
        first_dict = {'ID': id, 'DATA': first_msg}
        resultdict = self.SendMsgForResp(first_dict, dstcanid)
        result = resultdict.get('DATA')
        if result[0] == '30' or result[0] == '0A':
            childlist = msglist[6:]
            index = 21
            for child in range(0, len(childlist), 7):
                nextlist = childlist[child:child + 7]
                if len(nextlist) < 7:
                    nextlist = [str(index)] + nextlist + ['FF'] * (7 - len(nextlist))
                    enddict = {'ID': id, 'DATA': nextlist}
                    result = self.SendMsgForResp(enddict, dstcanid)
                    return result
                else:
                    nextdict = {'ID': id, 'DATA': [str(index)] + nextlist}
                    self.WriteFrame(nextdict)
                    index += 1
                    time.sleep(0.03)
        else:
            return []
            self.logger.info('send flow msg error')

    def send_flow_msg(self, id, msg):
        MsgDict = self.get_can_msg(id, msg)
        if len(msg) <= 16:
            result = self.SendMsgForResp(MsgDict,id)
        else:
            result = self.hanld_flow_msg(MsgDict)
        return result

    def clearlist(self):
        db_session = Common.CommonVar.Session()
        cantask = db_session.query(CanTask)
        cantask.delete(synchronize_session=False)
        db_session.commit()

    def auth(self):
        try:
            #切换通道
            self.SendMsgForResp(self.ext_CANmsg, '71c')
            time.sleep(0.01)
            #发送keep msg
            #self.SendMsgForResp(keep_CANmsg)
            # 发送鉴权
            seedlist = self.SendMsgForResp(self.seed_CANmsg, '71c')
            time.sleep(0.01)
            seedList = seedlist.get('DATA')
            seedList.pop()
            seedStr = ''.join(seedList)
            # print(int(seedStr, 16))
            seedCalc = c_ulong(int(seedStr, 16))
            self.sa.Seed2Key.restype = c_ulong
            #生成二次挑战码
            keyRst = self.sa.Seed2Key(seedCalc, c_int(1))
            # print(keyRst, hex(keyRst))
            keyStr = str((hex(keyRst)))[2:]
            lenth = len(keyStr)

            DiagDict['key_CANmsg']['ID'] = '714'

            for i in range(4):
                if (lenth - (2 * i)) > 0:
                    DiagDict['key_CANmsg']['DATA'][6 - i] = keyStr[-(2 * (i + 1)):(lenth - (2 * i))].zfill(2)
                else:
                    DiagDict['key_CANmsg']['DATA'][6 - i] = '00'
            rstData = self.SendMsgForResp(DiagDict['key_CANmsg'], '71c')
            time.sleep(0.01)
            if len(rstData) > 0:
                #logger.info('诊断CAN鉴权成功')
                self.logger.info('诊断CAN鉴权成功')
                return (True, '')
            else:
                #logger.info('诊断CAN鉴权失败')
                self.logger.info('诊断CAN鉴权失败')
        except Exception as e:
            #logger.info('诊断CAN鉴权失败:%s' % e)
            self.logger.info('诊断CAN鉴权失败')
            reason = str(e)
            return (False, reason)


if __name__ == '__main__':
    can_api = CANAPI_5G()
    """FF FF FF FF 34 36 30 30 30 30 
31 38 31 30 39 32 38 35 36 38 36 FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF 01
"""
    network_msg = {'ID': '41F', 'DATA': ['02', '70', '01', '00', '00', '00', '00', '00']}
    can_api.Timing_send_can(network_msg, 0.010, display=0)
    while 1:

        seedcmd = {'ID': '714', 'DATA': ['03', '22', 'B0', '01', '00', '00', '00', '00']}
        result = can_api.SendMsgFormanyResp(seedcmd, '71c')
        print(result)
        time.sleep(5)
    diag.close()