# coding:utf-8
from API.pyCAN1432 import *
from ResponseMap.Can_Map import *
import Common.CommonVar
from Common.CommonVar import logger



# =================================================
ext_CANmsg = {'ID':'711', 'DATA':['02', '10', '03', '00', '00', '00', '00', '00']}
extResp_CANmsg = {'ID':'719', 'DATA':['06', '50', '03']}
# =================================================
keep_CANmsg = {'ID':'711', 'DATA':['02', '00', '80', '00', '00', '00', '00', '00']}
# =================================================
#第一次鉴权
seed_CANmsg = {'ID':'711', 'DATA':['02', '27', '01', '00', '00', '00', '00', '00']}
seedResp_CANmsg = {'ID':'719', 'DATA':['06', '67', '01']}
# =================================================
#二次挑战
key_CANmsg = {'ID':'711', 'DATA':['06', '27', '02', '00', '00', '00', '00', '00']}
keyResp_CANmsg = {'ID':'719', 'DATA':['02', '67', '02']}
# =================================================
wake_CANmsg = {'ID':'41F', 'DATA':['02', '70', '01', '00', '00', '00', '00', '00']}
# =================================================
std_CANmsg = {'ID':'711', 'DATA':['02', '10', '01', '00', '00', '00', '00', '00']}
stdResp_CANmsg = {'ID':'719', 'DATA':['06', '50', '01']}
# =================================================
eolin1_CANmsg = {'ID':'711', 'DATA':['04', '31', '01', 'AF', 'F7', '00', '00', '00']}
eolin1Resp_CANmsg = {'ID':'719', 'DATA':['04', '71', '01', 'AF', 'F7']}
# =================================================
eolin2_CANmsg = {'ID':'711', 'DATA':['04', '31', '03', 'AF', 'F7', '00', '00', '00']}
eolin2Resp_CANmsg = {'ID':'719', 'DATA':['05', '71', '03', 'AF', 'F7']}
# =================================================
writeB210_CANmsg = {'ID':'6E1', 'DATA':['0A', '03', '18', '04', '0F', '00', '00', '00']}
writeB210Resp_CANmsg = {'ID':'6E9', 'DATA':['8A', '03']}
# =================================================
writeB210bak_CANmsg = {'ID':'6E1', 'DATA':['0A', '03', '19', '04', '0F', '00', '00', '00']}
writeB210bakResp_CANmsg = {'ID':'6E9', 'DATA':['8A', '03']}
# =================================================
writeF18C_01_CANmsg = {'ID': '6E1',  'DATA': ['0A', '01', '07', '10', '20', '37', '48', '34']}
writeF18C_02_CANmsg = {'ID': '6E1',  'DATA': ['0A', '21', '38', '38', '30', '44', '4A', '43']}
writeF18C_03_CANmsg = {'ID': '6E1',  'DATA': ['0A', '22', '31', '36', '42', '30', '35', '33']}
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
writeC009_01_CANmsg = {'ID':'6E1', 'DATA':['0A', '01', '36', '06', '34', '30', '30', '30']}
writeC009_02_CANmsg = {'ID':'6E1', 'DATA':['0A', '21', '34', '00', '00', '00', '00', '00']}
writeC009_01_Resp_CANmsg = {'ID':'6E9', 'DATA':['8A', '01', '01']}
writeC009_02_Resp_CANmsg = {'ID':'6E9', 'DATA':['8A', '01', '21']}
# =================================================
reset_CANmsg = {'ID':'711', 'DATA':['02', '11', '01', '00', '00', '00', '00', '00']}
resetResp_CANmsg = {'ID':'719', 'DATA':['02', '51', '01']}
# =================================================
eolout1_CANmsg = {'ID':'6E1', 'DATA':['01', '01', '00', '00', '00', '00', '00', '00']}
eolout1Resp_CANmsg = {'ID':'6E9', 'DATA':['81', '01']}
# =================================================
eolout2_CANmsg = {'ID':'6E1', 'DATA':['01', '02', '00', '00', '00', '00', '00', '00']}
eolout2Resp_CANmsg = {'ID':'6E9', 'DATA':['81', '02']}
# =================================================
writeB200_CANmsg = {'ID':'6E1', 'DATA':['0A', '03', '16', '02', '02', '08', '00', '00']}
writeB200Resp_CANmsg = {'ID':'6E9', 'DATA':['8A', '03']}
#==================================================
writeB200bak_CANmsg = {'ID':'6E1', 'DATA':['0A', '03', '17', '02', '02', '08', '00', '00']}
writeB200bakResp_CANmsg = {'ID':'6E9', 'DATA':['8A', '03']}
#==================================================
TelmcsRmtCtrlPotcl = {'01':'Request', '03':'','06':'','07':''}
BCMRmtCtrlPotcl = {'01':'Request', '02':'','04':'','05':'','06':''}
#==================================================
_msg = {'ID':'40', 'DATA':['01', 'F1', '11', '01', '00', '00', '00', '00']}
rps_msg = {'ID':'21', 'DATA':['02', 'F1', '11', '22', '33', '44', '55', '66']}
#==================================================
#network_mode_h5
network_msg = {'ID':'41F','DATA':['02', '70', '01', '00', '00', '00', '00', '00']}
#PwrMdMstr
PwrMdMstr_msg = {'ID':'1F1','DATA':['00', '00', '00', '00', '02', '00', '00', '00']}
#GW_HSC5_BCM_FrP09
GW_HSC5_BCM_FrP09 = {'ID':'21D','DATA':['00', '00', '00', '00', '00', '00', '00', '00']}
#GW_HSC5_BCM_FrP04
GW_HSC5_BCM_FrP04 = {'ID':'46A','DATA':['00', '00', '00', '00', '00', '00', '40', '00']}
#GW_HSC5_ECM_FrP00
GW_HSC5_ECM_FrP00 = {'ID':'C9' ,'DATA':['00', '00', '00', '00', '00', '00', '00', '00']}

class BcmSimu(CANAPI):

    def __init__(self):
        CANAPI.__init__(self)
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Seed2Key_uniqe.dll")
        self.sa = windll.LoadLibrary(path)

    def init_data(self):
        session = Common.CommonVar.Session
        self.ecu_map = {}
        from DB.Can_table import EcuMsg, EcuMap
        ecuList = session.query(EcuMsg.msg_id, EcuMsg.msg_value, EcuMsg.cycle_time).filter_by(cycle=1).all()
        for line in ecuList:
            self.Timing_send({'ID':line[0],'DATA':line[1]}, line[2]/1000)



    def auth(self):
        try:
            #切换通道
            self.SendMsgForResp(ext_CANmsg)
            time.sleep(0.01)
            #发送keep msg
            #self.SendMsgForResp(keep_CANmsg)
            # 发送鉴权
            seedlist = self.SendMsgForResp(seed_CANmsg)
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
            for i in range(4):
                if (lenth - (2 * i)) > 0:
                    DiagDict['key_CANmsg']['DATA'][6 - i] = keyStr[-(2 * (i + 1)):(lenth - (2 * i))].zfill(2)
                else:
                    DiagDict['key_CANmsg']['DATA'][6 - i] = '00'
            rstData = self.SendMsgForResp(DiagDict['key_CANmsg'])
            time.sleep(0.01)
            if len(rstData) > 0:
                logger.info('诊断CAN鉴权成功')
                return (True, '')
            else:
                logger.info('诊断CAN鉴权失败')
        except Exception as e:
            logger.info('诊断CAN鉴权失败:%s' % e)
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

    def chanllege_response(self):
        pass

    def chanllege_ack(self):
        pass

    def cmd_map(self, data):
        self.nowdata = data
        id = data.get('ID')
        datalist = data.get('DATA')
        if (id, datalist[0]) in bcm_map:
            result = self.handle_msg(bcm_map.get((id, datalist[0])))
            return result
        else:
            return data

    def handle_msg(self, map_dict):
        sendmsg = {}
        sendmsg['ID'] = map_dict.get('ID')
        sendmsg['DATA'] = []
        for line in map_dict.get('DATA'):
            if 'get' not in line:
                sendmsg['DATA'].append(line)
            else:
                result = line()
                sendmsg['DATA']+result
        if len(sendmsg['DATA']) < 8:
            sendmsg['DATA'] = sendmsg['DATA'] + ['00']*(8-len(sendmsg['DATA']))
        return sendmsg

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
        for i in range(0,len(keyStr), 2):
            data.append(keyStr[i:i+2])
        return data


# class BcmStart(BaseHandler):
#
#     def get(self):
#         try:
#             can_api = BcmSimu()
#             result = {'result': 0, 'Conn': 1}
#             return_data = json.dumps(result, ensure_ascii=False)
#             self.write(return_data)
#         except Exception as e:
#             logger.info('Bcm 启动失败:%s' %e)
#             result = {'result': -1, 'Conn': 1}
#             return_data = json.dumps(result, ensure_ascii=False)
#             self.write(return_data)



if __name__ == '__main__':
    import sys
    sys.path.append(r'D:\AutoWeb\Auto_system\API')
    can_api = BcmSimu()

    result1 = can_api.auth()
    #can_api.SendMsgForResp({'ID':'711', 'DATA':['02', '10', '00', '00', '00', '00', '00', '00']})
    #rev = can_api.SendMsgForResp(rps_msg2)
    #print(result1)
    """FF FF FF FF 34 36 30 30 30 30 
31 38 31 30 39 32 38 35 36 38 36 FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF 01
"""
    MsgDict = {'ID': '711', 'DATA': ['10', '28', '2E', 'CA', '02', '34', '36', '30']}
    result = can_api.SendMsgForResp(MsgDict)
    #MsgDict2 = {'ID': '711', 'DATA': ['21', '30', '30', '30', '31', '33', '30', '38']}
    MsgDict2 = {'ID': '711', 'DATA': ['21', '30', '30', '30', '31', '35', '31', '39']}
    result = can_api.WriteFrame(MsgDict2)
    time.sleep(0.01)
    #MsgDict3 = {'ID': '711', 'DATA': ['22', '37' ,'36', '30', '38', '32', '38', '30']}
    MsgDict3 = {'ID': '711', 'DATA': ['22', '31', '34', '38', '33', '38', '36', '32']}
    result = can_api.WriteFrame(MsgDict3)
    time.sleep(0.01)
    MsgDict4 = {'ID': '711', 'DATA': ['23', 'AA', 'AA', 'AA','AA', 'FF', 'FF', 'FF']}
    result = can_api.WriteFrame(MsgDict4)
    time.sleep(0.01)
    MsgDict5 = {'ID': '711', 'DATA': ['24', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF']}
    result = can_api.WriteFrame(MsgDict5)
    time.sleep(0.01)
    MsgDict6 = {'ID': '711', 'DATA': ['25', 'FF', 'FF', 'FF', 'FF', 'FF', '00', 'AA']}
    time.sleep(0.01)
    result = can_api.SendMsgForResp(MsgDict6)

    print(result)

    # can_api.Timing_send(network_msg, 1)
    # can_api.Timing_send(PwrMdMstr_msg, 0.02)
    # can_api.Timing_send(GW_HSC5_BCM_FrP09, 0.05)
    # can_api.Timing_send(GW_HSC5_BCM_FrP04, 0.05)
    # can_api.Timing_send(GW_HSC5_ECM_FrP00, 0.01)
    # time.sleep(10)
    # # result = can_api.send_flow_msg('40', '0112021008000000')
    # MsgDict = {'ID': '711', 'DATA': ['10', '28', '2E', 'CA', '02','FF','FF','FF']}
    # result = can_api.SendMsgForResp(MsgDict)
    # MsgDict2 = {'ID': '711', 'DATA': [  '21', 'FF','34', '36', '30','30', '30', '30']}
    # result = can_api.WriteFrame(MsgDict2)
    # MsgDict3 = {'ID': '711', 'DATA': ['22', '31', '38', '31', '30', '39' ,'32', '38']}
    # result = can_api.WriteFrame(MsgDict3)
    # MsgDict4 = {'ID': '711', 'DATA': ['23', '35', '36', '38', '36','00', 'FF', 'FF']}
    # result = can_api.WriteFrame(MsgDict4)
    # MsgDict5 = {'ID': '711', 'DATA': ['24', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF']}
    # result = can_api.WriteFrame(MsgDict5)
    # MsgDict6 = {'ID': '711', 'DATA': ['25', 'FF', 'FF', 'FF', 'FF', 'FF', '01', 'AA']}
    #
    # result = can_api.SendMsgForResp(MsgDict6)
    # # result = can_api.hanld_flow_msg('FFFFFFFF3436303030303138313039323835363836FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF01')
    # print(result)
    while 1:
        pass
    can_api.btnRelease_Click()