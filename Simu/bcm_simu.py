# coding:utf-8
from urllib.parse import quote
from unidecode import unidecode

from API.pyCAN import *
from ResponseMap.Can_Map import *
import Common.CommonVar
from Common.CommonVar import logger
from Common.CommonVar import Session
from Simu.avn_simu import *
from DB.Can_table import *
from tornado.concurrent import run_on_executor
from tornado import gen
from ResponseMap.bcm_Response import *

# =================================================
ext_CANmsg = {'ID': '711', 'DATA': ['02', '10', '03', '00', '00', '00', '00', '00']}
extResp_CANmsg = {'ID': '719', 'DATA': ['06', '50', '03']}
# =================================================
keep_CANmsg = {'ID': '711', 'DATA': ['02', '00', '80', '00', '00', '00', '00', '00']}
# =================================================
# 第一次鉴权
seed_CANmsg = {'ID': '711', 'DATA': ['02', '27', '01', '00', '00', '00', '00', '00']}
seedResp_CANmsg = {'ID': '719', 'DATA': ['06', '67', '01']}
# =================================================
# 二次挑战
key_CANmsg = {'ID': '711', 'DATA': ['06', '27', '02', '00', '00', '00', '00', '00']}
keyResp_CANmsg = {'ID': '719', 'DATA': ['02', '67', '02']}
# =================================================
wake_CANmsg = {'ID': '41F', 'DATA': ['02', '70', '01', '00', '00', '00', '00', '00']}
# =================================================
std_CANmsg = {'ID': '711', 'DATA': ['02', '10', '01', '00', '00', '00', '00', '00']}
stdResp_CANmsg = {'ID': '719', 'DATA': ['06', '50', '01']}
# =================================================
eolin1_CANmsg = {'ID': '711', 'DATA': ['04', '31', '01', 'AF', 'F7', '00', '00', '00']}
eolin1Resp_CANmsg = {'ID': '719', 'DATA': ['04', '71', '01', 'AF', 'F7']}
# =================================================
eolin2_CANmsg = {'ID': '711', 'DATA': ['04', '31', '03', 'AF', 'F7', '00', '00', '00']}
eolin2Resp_CANmsg = {'ID': '719', 'DATA': ['05', '71', '03', 'AF', 'F7']}
# =================================================
writeB210_CANmsg = {'ID': '6E1', 'DATA': ['0A', '03', '18', '04', '0F', '00', '00', '00']}
writeB210Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '03']}
# =================================================
writeB210bak_CANmsg = {'ID': '6E1', 'DATA': ['0A', '03', '19', '04', '0F', '00', '00', '00']}
writeB210bakResp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '03']}
# =================================================
writeF18C_01_CANmsg = {'ID': '6E1', 'DATA': ['0A', '01', '07', '10', '20', '37', '48', '34']}
writeF18C_02_CANmsg = {'ID': '6E1', 'DATA': ['0A', '21', '38', '38', '30', '44', '4A', '43']}
writeF18C_03_CANmsg = {'ID': '6E1', 'DATA': ['0A', '22', '31', '36', '42', '30', '35', '33']}
writeF18C_01_Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '01', '01']}
writeF18C_02_Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '01', '21']}
writeF18C_03_Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '01', '22']}
# =================================================
writeF190_01_CANmsg = {'ID': '6E1', 'DATA': ['0A', '01', '08', '14', '4C', '53', '4A', '57']}
writeF190_02_CANmsg = {'ID': '6E1', 'DATA': ['0A', '21', '35', '34', '44', '4A', '43', '31']}
writeF190_03_CANmsg = {'ID': '6E1', 'DATA': ['0A', '22', '36', '42', '30', '30', '30', '35']}
writeF190_04_CANmsg = {'ID': '6E1', 'DATA': ['0A', '23', '30', '00', '00', '00', '00', '00']}
writeF190_01_Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '01', '01']}
writeF190_02_Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '01', '21']}
writeF190_03_Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '01', '22']}
writeF190_04_Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '01', '23']}
# =================================================
writeC009_01_CANmsg = {'ID': '6E1', 'DATA': ['0A', '01', '36', '06', '34', '30', '30', '30']}
writeC009_02_CANmsg = {'ID': '6E1', 'DATA': ['0A', '21', '34', '00', '00', '00', '00', '00']}
writeC009_01_Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '01', '01']}
writeC009_02_Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '01', '21']}
# =================================================
reset_CANmsg = {'ID': '711', 'DATA': ['02', '11', '01', '00', '00', '00', '00', '00']}
resetResp_CANmsg = {'ID': '719', 'DATA': ['02', '51', '01']}
# =================================================
eolout1_CANmsg = {'ID': '6E1', 'DATA': ['01', '01', '00', '00', '00', '00', '00', '00']}
eolout1Resp_CANmsg = {'ID': '6E9', 'DATA': ['81', '01']}
# =================================================
eolout2_CANmsg = {'ID': '6E1', 'DATA': ['01', '02', '00', '00', '00', '00', '00', '00']}
eolout2Resp_CANmsg = {'ID': '6E9', 'DATA': ['81', '02']}
# =================================================
writeB200_CANmsg = {'ID': '6E1', 'DATA': ['0A', '03', '16', '02', '02', '08', '00', '00']}
writeB200Resp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '03']}
# ==================================================
writeB200bak_CANmsg = {'ID': '6E1', 'DATA': ['0A', '03', '17', '02', '02', '08', '00', '00']}
writeB200bakResp_CANmsg = {'ID': '6E9', 'DATA': ['8A', '03']}
# ==================================================
TelmcsRmtCtrlPotcl = {'01': 'Request', '03': '', '06': '', '07': ''}
BCMRmtCtrlPotcl = {'01': 'Request', '02': '', '04': '', '05': '', '06': ''}
# ==================================================
auth01 = {'ID': '40', 'DATA': ['01', 'F1', '11', '01', '00', '00', '00', '00']}
rps_msg = {'ID': '21', 'DATA': ['02', 'F1', '11', '22', '33', '44', '55', '66']}
# ==================================================
# network_mode_h5
network_msg = {'ID': '41F', 'DATA': ['02', '70', '01', '00', '00', '00', '00', '00']}
# PwrMdMstr
# 00 00 00 00 02 00 00 00
PwrMdMstr_msg = {'ID': '1F1', 'DATA': ['0C', '00', '00', '00', '02', '00', '00', '00']}
# GW_HSC5_BCM_FrP09
GW_HSC5_BCM_FrP09 = {'ID': '21D', 'DATA': ['00', '00', '00', '00', '00', '00', '00', '00']}
# GW_HSC5_BCM_FrP04
GW_HSC5_BCM_FrP04 = {'ID': '46A', 'DATA': ['00', '00', '00', '00', '00', '00', '40', '00']}
# GW_HSC5_BCM_FrP04 = {'ID':'46A','DATA':['00', '00', '00', '00', '00', '00', '00', '00']}
# GW_HSC5_ECM_FrP00
GW_HSC5_ECM_FrP00 = {'ID': 'C9', 'DATA': ['00', '00', '00', '00', '00', '00', '00', '00']}


class BcmSimu(CANAPI):
    instancesobj = None

    def __init__(self):
        CANAPI.__init__(self)

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Seed2Key_uniqe.dll")
        self.sa = windll.LoadLibrary(path)
        self.bcm_map = self.bcm_map_db()
        self.bcmMsg = self.bcm_msg_db()
        pass

    def bcm_msg_db(self):
        session = Common.CommonVar.Session()
        bcmMsg = {}
        msgdb = session.query(EcuMsg.msg_id, EcuMsg.msg_value, EcuMsg.msg_name, EcuMsg.cycle,
                              EcuMsg.cycle_time, EcuMsg.len, EcuMsg.count, EcuMsg.delaytime, EcuMsg.Intervaltime).all()
        for index, line in enumerate(msgdb):
            bcmMsg[line[2]] = {'id': index + 1, 'ID': line[0], 'DATA': line[1], 'name': line[2],
                               'cycle': str(line[3]), 'cycle_time': line[4], 'len': line[5],
                               'count': line[6], 'delaytime': line[7], 'Intervaltime': line[8]}

        return bcmMsg

    def bcm_map_db(self):
        session = Common.CommonVar.Session()
        ecu_map = {}
        from DB.Can_table import EcuMsg, EcuMap, EcuMsg
        ecuList = session.query(EcuMap.cmd_Resp, EcuMap.map_func, EcuMap.related_ecu_msg).all()
        for line in ecuList:
            msg_index = eval(line[0])
            msg_func = line[1]
            msg_para = line[2].split(',')
            msg_dict = []
            for para in msg_para:
                para_dict = {}
                # {'ID':'21','DATA':['02', 'get_handle', 'get_challenge']}
                ecuList = session.query(EcuMsg.msg_id, EcuMsg.msg_value, EcuMsg.msg_name). \
                    filter_by(msg_name=para).first()
                if ecuList:
                    para_dict['ID'] = ecuList[0]
                    para_dict['DATA'] = eval(ecuList[1])
                    msg_dict.append(para_dict)
                # para_name = ecuList[2]
                # msg_dict[para_name] = para_dict
            ecu_map[msg_index] = [msg_func, msg_dict]

        return ecu_map

    def init_data(self):
        session = Common.CommonVar.Session
        self.ecu_map = {}
        from DB.Can_table import EcuMsg, EcuMap
        ecuList = session.query(EcuMsg.msg_id, EcuMsg.msg_value, EcuMsg.cycle_time).all()
        for line in ecuList:
            self.Timing_send({'ID': line[0], 'DATA': line[1]}, line[2] / 1000)

    def auth(self):
        try:
            # 切换通道
            self.SendMsgForResp(ext_CANmsg)
            # 发送keep msg
            # self.SendMsgForResp(keep_CANmsg)
            # 发送鉴权
            seedlist = self.SendMsgForResp(seed_CANmsg)
            seedList = seedlist.get('DATA')
            seedList.pop()
            seedStr = ''.join(seedList)
            # print(int(seedStr, 16))
            seedCalc = c_ulong(int(seedStr, 16))
            self.sa.Seed2Key.restype = c_ulong
            # 生成二次挑战码
            keyRst = self.sa.Seed2Key(seedCalc, c_int(1))
            # print(keyRst, hex(keyRst))
            keyStr = str((hex(keyRst)))[2:]
            lenth = len(keyStr)
            for i in range(4):
                if (lenth - (2 * i)) > 0:
                    DiagDict['key_CANmsg']['DATA'][6 - i] = keyStr[-(2 * (i + 1)):(lenth - (2 * i))].zfill(2)
                else:
                    DiagDict['key_CANmsg']['DATA'][6 - i] = '00'
            rstData = self.SendMsgForResp(DiagDict['key_CANmsg'])
            if len(rstData) > 0:
                self.logger.info('诊断CAN鉴权成功')
                return (True, '')
            else:
                self.logger.info('诊断CAN鉴权失败')
        except Exception as e:
            self.logger.info('诊断CAN鉴权失败:%s' % e)
            reason = str(e)
        return (False, reason)

    def get_chanllege_data(self, seedList):
        seedStr = ''.join(seedList)
        # print(int(seedStr, 16))
        seedCalc = c_ulong(int(seedStr, 16))
        self.sa.Seed2Key.restype = c_ulong
        # 生成二次挑战码
        keyRst = self.sa.Seed2Key(seedCalc, c_int(1))
        # print(keyRst, hex(keyRst))
        keyStr = str((hex(keyRst)))[2:]
        return

    def get_DTC(self):
        MsgDict = {'ID': '711', 'DATA': ['03', '19', '02', '7F', 'FF', 'FF', 'FF', 'FF']}
        dtclist = self.SendMsgForResp(MsgDict)
        result = ''
        for line in dtclist:
            result += ''.join(line.get('DATA'))
        return result

    def Timing_after(self):
        time.sleep(40)
        if self.setDict:
            for cankey in self.setDict:
                self.bcmMsg[cankey]['DATA'] = self.setDict.get(cankey)

    def Timing_send(self, name, display=1):
        try:
            # self.timing_send = Thread(target=self.TimingMsg, args=(msg,timing))
            # self.timing_send.daemon = True
            # self.timing_send.start()
            # yield self.TimingMsg(name,timing,count,Intervaltime,delaytime)
            msg_time = int(self.bcmMsg.get(name).get('cycle_time')) / 1000
            if msg_time < 1:
                display = 0.5 / msg_time
            else:
                display = 1
            self.thread_pool.submit(self.TimingMsg, name, display)
        except Exception as e:
            self.logger.info('Timing_send error:%s' % e)

    @run_on_executor
    def TimingMsg(self, name, display):
        count = self.bcmMsg.get(name).get('count')
        delaytime = self.bcmMsg.get(name).get('delaytime')
        Intervaltime = self.bcmMsg.get(name).get('cycle_time')
        if count != -1:
            while count:
                if not self.enable:
                    break
                count = self.bcmMsg.get(name).get('count')
                delaytime = self.bcmMsg.get(name).get('delaytime')
                Intervaltime = self.bcmMsg.get(name).get('cycle_time')
                time.sleep(delaytime)
                timedata = Intervaltime if Intervaltime else delaytime
                self.WriteFrame(self.bcmMsg.get(name), timedata)
                time.sleep(Intervaltime)
                count -= 1
        else:
            i = 1

            while count == -1:
                if not self.enable:
                    break
                count = self.bcmMsg.get(name).get('count')
                delaytime = self.bcmMsg.get(name).get('delaytime')
                Intervaltime = int(self.bcmMsg.get(name).get('cycle_time')) / 1000

                msg = self.bcmMsg.get(name)
                if i == display:
                    self.WriteFrame(msg, Intervaltime, display=True)
                    i = 0
                else:
                    self.WriteFrame(msg, Intervaltime, display=False)
                i += 1
                time.sleep(Intervaltime)

    @run_on_executor
    def TimingMsgInput(self, msg, timing, count=-1, Intervaltime=0, delaytime=0, display=1):
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
                    i = 0
                else:
                    self.WriteFrame(msg, timing, display=False)
                i += 1
                time.sleep(timing)

    def handle_app_msg(self, msg):
        handle = msg.get('DATA')[1]
        sendData = {}
        if msg.get('DATA')[0] == '01':
            sendData['ID'] = '21'
            sendData['DATA'] = []
            sendData['DATA'].append('02')
            sendData['DATA'].append(handle)
            sendData['DATA'] += ['11', '22', '33', '44', '55', '66']
        elif msg.get('DATA')[0] == '03':
            sendData['ID'] = '21'
            sendData['DATA'] = []
            sendData['DATA'].append('04')
            sendData['DATA'].append(handle)
            sendData['DATA'] += ['02', '00', '00', '00', '00', '00']
        elif msg.get('DATA')[0] == '05':
            sendData['ID'] = '21'
            sendData['DATA'] = []
            sendData['DATA'].append('06')
            sendData['DATA'].append(handle)
            sendData['DATA'] += ['02', '00', '00', '00', '00', '00']
        self.SendMsgForResp(sendData, '21')

    def chanllege_response(self):
        pass

    def chanllege_ack(self):
        pass

    def cmd_map(self, data, db):
        id = data.get('ID')
        datalist = data.get('DATA')
        result = []
        if (id, datalist[0]) in self.bcm_map:
            func_type = eval(self.bcm_map.get((id, datalist[0]))[0])
            args_dict = self.bcm_map.get((id, datalist[0]))[1]
            func_type(*args_dict, Msg=data, sendMsg=self.WriteFrame, self=self)

    def Bcm_Start(self):
        BcmSimu.instancesobj = self.get_instances()

        self.Timing_send('net_work')
        self.Timing_send('PwrMdMstr')
        self.Timing_send('GW_hsc5_09')
        self.Timing_send('GW_hsc5_04')
        self.Timing_send('GW_hsc5_00')
        # self.Timing_send('TBOX_HSC5_FrP01',
        #                  int(self.bcmMsg.get('TBOX_HSC5_FrP01').get('cycle_time'))/1000)
    def Bcm_Stop(self):
        print(self.enable)
        print(self.REV_FLAG)
        print(self.SEND_FLAG)
        print(BcmSimu.instancesobj)

        self.enable = 0
        self.REV_FLAG = 0
        self.SEND_FLAG = 0
        BcmSimu.instancesobj = None
        self.btnRelease_Click()
    def start_fire(self):
        self.bcmMsg['PwrMdMstr']['DATA'] = \
            self.bcmMsg['PwrMdMstr_ON']['DATA']

    def stop_fire(self):
        self.bcmMsg['PwrMdMstr']['DATA'] = \
            self.bcmMsg['PwrMdMstr_off']['DATA']

    def KL15_ON(self):
        self.bcmMsg['PwrMdMstr']['DATA'] = \
            self.bcmMsg['PwrMdMstr_off']['DATA']

    def KL15_OFF(self):
        self.bcmMsg['PwrMdMstr']['DATA'] = \
            self.bcmMsg['PwrMdMstr_off']['DATA']

    def get_handle(self):
        return [self.nowdata.get('DATA')[1]]

    def get_challenge(self):
        data = []
        self.BCMRequestType = self.nowdata.get('DATA')[2]
        self.BCMRequestParameters = self.nowdata.get('DATA')[3:]
        seedStr = ''.join(self.nowdata.get('DATA'))
        seedCalc = c_ulong(int(seedStr, 16))
        self.sa.Seed2Key.restype = c_ulong
        # 生成二次挑战码
        keyRst = self.sa.Seed2Key(seedCalc, c_int(1))
        keyStr = str((hex(keyRst)))[2:]
        for i in range(0, len(keyStr), 2):
            data.append(keyStr[i:i + 2])
        return data

    @staticmethod
    def get_instances():
        if not BcmSimu.instancesobj:
            BcmSimu.instancesobj = BcmSimu()
        return BcmSimu.instancesobj


class GetBcmData(BaseHandler):

    def post(self):
        try:
            # self.logger .info('Bcm 获取数据开始')
            result = self.response_msg()
            return_data = json.dumps(result, ensure_ascii=False)
            # self.logger .info('Bcm 获取数据结束')
            self.write(return_data)
        except Exception as e:
            self.logger.info('Bcm 获取数据失败:%s' % e)
            result = {'result': -1, 'Conn': 1}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

    def response_msg(self):
        session = Common.CommonVar.Session()
        bcm_data = session.query(CanTask).all()
        bcm_new_data = self.db_2_vue(bcm_data)
        if BcmSimu.instancesobj:
            bcmMsg = list(BcmSimu.instancesobj.bcmMsg.values())
        else:
            bcmMsg = []
        result = {'bmc_data': bcm_new_data, 'child_data': {}, 'bmc_MSG': bcmMsg}

        return result

    def db_2_vue(self, avn_data):
        result = []

        for pid, vue_line in enumerate(avn_data, start=1):
            line = vue_line.__dict__
            result_line = {}
            try:
                for i in line:
                    if i == '_sa_instance_state':
                        pass
                    elif i == 'id':
                        result_line[i] = pid
                    elif i == 'current':
                        result_line[i] = str(line.get(i))
                    else:
                        result_line[i] = line.get(i)
                result.append(result_line)
            except Exception as e:
                pass
        return result


class startBcm(BaseHandler):

    def post(self):
        try:
            state = self.get_argument('state')
            return_data = self.response_msg(state)
            self.write(return_data)
        except Exception as e:
            self.logger.info('Bcm 启动失败:%s' % e)
            result = {'result': -1, 'Conn': 1}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

    def response_msg(self, state):
        if state == '1':
            self.logger.info('Bcm 启动开始')
            bcm_obj = BcmSimu.get_instances()
            self.logger.info('Bcm 启动关闭')
            result = {'result': 0, 'Conn': 1}
        elif state == '2':
            bcm_obj = BcmSimu.get_instances()
            bcm_obj.close('bcm')
            del bcm_obj
            BcmSimu.instancesobj = None
            result = {'result': 0, 'Conn': 0}
        else:
            bcm_obj = BcmSimu.get_instances()
            bcm_obj.close()
            del bcm_obj
            BcmSimu.instancesobj = None
            result = {'result': 0, 'Conn': 0}

        return_data = json.dumps(result, ensure_ascii=False)
        return return_data


class execute(BaseHandler):

    def post(self):
        try:
            ex_value = self.get_argument('ex_value')
            if ex_value:


                funcname = ex_value.split(':')[0]
                para = ex_value.split(':')[1:]
                bcm_obj = BcmSimu.get_instances()

                getattr(bcm_obj, funcname)(*para)
                result = {'result': 0}

            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)
        except Exception as e:
            self.logger.info('Bcm execute 执行命令失败:%s' % e)
            result = {'result': -1}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)


class init_Bcm(BaseHandler):

    def post(self):
        try:
            ex_value = self.get_argument('ex_value')
            if ex_value:
                if ':' in ex_value:
                    paralist = ex_value.split(':')[1].split(',')
                else:
                    paralist = []
                para = []
                for line in paralist:
                    if line.isdigit():
                        para.append(int(line))
                    else:
                        para.append(eval(line))
                funcname = ex_value.split(':')[0]
                bcm_obj = BcmSimu.get_instances()
                getattr(bcm_obj, funcname)(*para)
                result = {'result': 0, 'Conn': 2}

            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)
        except Exception as e:
            self.logger.info('Bcm init_Bcm执行命令失败:%s' % e)
            result = {'result': -1, 'Conn': 1}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)


class sendCan(BaseHandler):

    @gen.coroutine
    def post(self):
        try:
            srccanid = self.get_argument('srccanid')
            dstcanid = self.get_argument('dstcanid')
            cantextList = self.get_argument('cantext').split(';')
            cycle_time = self.get_argument('cycle_time')
            for cantext in cantextList:

                return_data = self.response_msg(cantext, srccanid, dstcanid, int(cycle_time))

            self.write(return_data)
        except Exception as e:
            self.logger.info('Bcm sendCan执行命令失败:%s' % e)
            result = {'result': -1}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

    def response_msg(self, cantext, srccanid, dstcanid, cycle_time):
        bcm_obj = BcmSimu.get_instances()
        msg = {}
        if len(cantext) <= 8:
            msg['ID'] = srccanid
            canmsg = [cantext[i:i + 2] for i in range(0, len(cantext), 2)]
            msg['DATA'] = canmsg + ['00'] * (8 - len(canmsg))
            if not cycle_time:
                bcm_obj.SendMsgForResp(msg, dstcanid)
            else:
                msg_time = int(cycle_time) / 1000
                if msg_time < 1:
                    display = 1 / msg_time
                else:
                    display = 1
                bcm_obj.thread_pool.submit(bcm_obj.TimingMsgInput, msg, msg_time, -1, cycle_time, 0, display)
            result = {'result': 0}
        else:
            msg['ID'] = srccanid
            msg['DATA'] = cantext
            if not cycle_time:
                data = bcm_obj.hanld_flow_msg(msg, dstcanid)
            else:
                data = ''
            result = {'result': 0, 'data': data}
        return_data = json.dumps(result, ensure_ascii=False)
        return return_data


class ClearList(BaseHandler):

    def post(self):
        try:
            bcm_obj = BcmSimu.get_instances()
            bcm_obj.clearlist()
            result = {'result': 0}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)
        except Exception as e:
            self.logger.info('Bcm ClearList执行命令失败:%s' % e)
            result = {'result': -1}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)


class SaveData(BaseHandler):

    def post(self):
        try:
            msgdict = eval(self.get_argument('candict'))
            bcm_obj = BcmSimu.get_instances()
            name = msgdict.get('name')
            bcm_obj.bcmMsg[name] = msgdict
            result = {'result': 0}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)
        except Exception as e:
            self.logger.info('Bcm SaveData执行命令失败:%s' % e)
            result = {'result': -1}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)


class download(BaseHandler):

    def get(self):
        try:
            filename = self.get_argument('filename')
            filepath = os.path.join(os.environ['root_path'],'Log',filename)

            return_data = self.loadfile(filepath)

            self.finish()
        except Exception as e:
            self.logger.info('Bcm download执行命令失败:%s' % e)
            result = {'result': -1}
            return_data = json.dumps(result, ensure_ascii=False)

            self.write(return_data)

    def loadfile(self, filename):
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', "attachment;filename=%s; filename*=UTF-8''%s" % (
            unidecode(filename).replace(' ', '_'), quote(filename)))
        # 读取的模式需要根据实际情况进行修改
        with open(filename, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                self.write(data)

    # def loadfile2(self,filename):
    #     # 读取的模式需要根据实际情况进行修改
    #     response = FileResponse(open(filename, 'rb'))
    #     response['Content-Type'] = 'application/octet-stream'
    #     response['Access-Control-Allow-Origin'] = '*'
    #     # response['Content-Encoding'] = 'gzip'
    #     response['Content-Disposition'] = "attachment;filename=%s; filename*=UTF-8''%s" % (
    #         unidecode(file_name).replace(' ', '_'), quote(file_name))
    #     return response
    # if __name__ == '__main__':
    #     can_api = BcmSimu()
    #
    #     result1 = can_api.auth()
    # can_api.SendMsgForResp({'ID':'711', 'DATA':['02', '10', '00', '00', '00', '00', '00', '00']})
    # rev = can_api.SendMsgForResp(rps_msg2)
    # print(result1)
    """FF FF FF FF 34 36 30 30 30 30 
31 38 31 30 39 32 38 35 36 38 36 FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF 01
"""
    # MsgDict = {'ID': '711', 'DATA': ['10', '28', '2E', 'CA', '02', '34', '36', '30']}
    # result = can_api.SendMsgForResp(MsgDict)
    # MsgDict2 = {'ID': '711', 'DATA': ['21', '30', '30', '30', '31', '38', '31', '30']}
    # result = can_api.WriteFrame(MsgDict2)
    # MsgDict3 = {'ID': '711', 'DATA': ['22', '39' ,'32', '38', '35', '36', '38', '36']}
    # result = can_api.WriteFrame(MsgDict3)
    # MsgDict4 = {'ID': '711', 'DATA': ['23', '00', '00', '00','00', 'FF', 'FF', 'FF']}
    # result = can_api.WriteFrame(MsgDict4)
    # MsgDict5 = {'ID': '711', 'DATA': ['24', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF']}
    # result = can_api.WriteFrame(MsgDict5)
    # MsgDict6 = {'ID': '711', 'DATA': ['25', 'FF', 'FF', 'FF', 'FF', 'FF', '01', 'AA']}
    #
    # result = can_api.SendMsgForResp(MsgDict6)
    #
    # print(result)

    # can_api.Timing_send(network_msg, 1)
    # can_api.Timing_send(PwrMdMstr_msg, 0.02)
    # can_api.Timing_send(GW_HSC5_BCM_FrP09, 0.05)
    # can_api.Timing_send(GW_HSC5_BCM_FrP04, 0.05)
    # can_api.Timing_send(GW_HSC5_ECM_FrP00, 0.01)
    # # time.sleep(10)
    # # result = can_api.send_flow_msg('40', '0112021008000000')
    # while 1:
    #     pass
    # can_api.btnRelease_Click()
