# coding:utf-8

import os
from Communication.SocketClient import BaseClient
from Common.CommonVar import logger,SINGLE
from Common.CommonFun import *
from binascii import hexlify, unhexlify
import time, datetime
try:
    from DB.avn_table import AvnSimu as avn
except:
    pass
#from DB.avn_table import AvnPara
import Common.CommonVar
import binascii
import json
from tornado.concurrent import run_on_executor
import pandas as pd
from API.Logger import Loggers
from API.Py_excle import *

class USBIAgree(BaseClient):
    instancesobj = {}

    def __init__(self, host, port):
        BaseClient.__init__(self, host, port)
        rootpath = os.environ['root_path']
        logpath = os.path.join(rootpath, 'Log')
        cfg = pyExcel.get_instances()
        self.logger = Loggers.get_instances(filename='avn_4g.log', log_dir=logpath,
                                    logtype=cfg.get_cfgkey_value('avn_logtype'))
        self.db_session = Common.CommonVar.Session()
        self.nosendlist = []
        self.reset_para =''

    def parse_cmd(self, msg):
        rev_msg = decode(hexlify(encode(msg)))
        if '0315' in rev_msg:
            pass
        cmd = self.split_msg(rev_msg)
        return cmd

    def split_msg(self, msg):
        cmdlist = []
        if '18' != msg[:2]:
            raise

        else:
            msglen = int(msg[4:6] + msg[2:4], 16) * 2
            if len(msg) == msglen:
                cmdlist = [msg[8:10] + msg[6:8]]
            elif len(msg) > msglen:
                childmsg = msg[:msglen]
                cmdlist.append([childmsg[8:10] + childmsg[6:8]])
                cmdlist += self.split_msg(msg[msglen:])

        return cmdlist

    @run_on_executor
    def QueryCurWANConnInfo(self, msg, id):
        try:
            wan_status = msg[14:]
            db_content = self.get_wan(wan_status)
            self.set_db_data(db_content, id,'avnpara')
        except Exception as e:
            logger.info('QueryCurWANConnInfo error:%s'%e)

    def get_wan(self, body_info):
        wan_status = body_info[0:2]
        wan_result = Common.CommonVar.WAN_STATUE.get(wan_status)
        wan_ip = body_info[2:]
        wan_ip_result = binascii.unhexlify(wan_ip.encode()).split(b'\x00')[0]

        db_content = {'信号状态': wan_result, 'IP地址': wan_ip_result.decode()}
        return db_content

    @run_on_executor
    def QueryCurGPSInfo(self, msg, id):
        try:
            body_info = msg[14:]
            result,index = self.get_gps(body_info)
            self.set_db_data(result, id,'avnpara')
        except Exception as e:
             logger.info('QueryCurGPSInfo error:%s'%e)

    def get_gps(self,body_info):
        gps_info = body_info
        timestamp = int(gps_info[0:8], 16)
        gpsStatus = int(gps_info[8:10], 16)
        heading = int(gps_info[10:14], 16)
        speed = int(gps_info[14:18], 16)
        pdop = int(gps_info[18:22], 16)
        hdop = int(gps_info[22:26], 16)
        vdop = int(gps_info[26:30], 16)
        satellites = int(gps_info[30:32], 16)
        latitude = int(gps_info[32:40], 16)
        longitude = int(gps_info[40:48], 16)
        altitude = int(gps_info[48:56], 16)
        satellitesInfo = gps_info[56:]
        satellites_list = []
        begin_index = 0
        for sateInfo in range(0, 24):
            sateInfoDict = {}
            sateInfoDict['SATELLITE_INVIEW_ID'] = int(satellitesInfo[begin_index:begin_index + 2], 16)
            sateInfoDict['EVALUATION'] = int(satellitesInfo[begin_index + 2:begin_index + 4], 16)
            sateInfoDict['AZIMUTH'] = int(satellitesInfo[begin_index + 4:begin_index + 8], 16)
            sateInfoDict['SNR'] = int(satellitesInfo[begin_index + 8:begin_index + 10], 16)
            sateInfoDict['IS_USED'] = int(satellitesInfo[begin_index + 10:begin_index + 12], 16)
            begin_index += 12
            satellites_list.append(sateInfoDict)
        result = {'timestamp': timestamp, 'gpsStatus': gpsStatus, 'heading': heading,
                  'speed': speed, 'pdop': pdop, 'hdop': hdop, 'vdop': vdop, 'satellites': satellites,
                  'latitude': latitude, 'longitude': longitude, 'altitude': altitude, 'satellitesInfo': satellites_list
                  }
        end_index = 56 + begin_index
        return result,end_index
    @run_on_executor
    def QueryCurBSInfo(self, msg, id):
        try:

            body_info = msg[14:]
            result,endindex = self.get_bts(body_info)
            self.set_db_data(result,id,'avnpara')
        except Exception as e:
            logger.info('QueryCurBSInfo error:%s' % e)

    def get_bts(self, body_info):
        result = {}
        BsInfocount = int(body_info[0:2], 16)
        BSInfo = {}
        begin_index = 0
        for baseinfo in range(0, int(BsInfocount)):
            BSInfo[baseinfo] = {}
            BSInfo[baseinfo]['net_type'] = Common.CommonVar.NET_TYPE.get(
                int(body_info[begin_index + 2:begin_index + 4], 16))
            BSInfo[baseinfo]['connected'] = Common.CommonVar.CELL_TYPE.get(
                int(body_info[begin_index + 4:begin_index + 6], 16))
            BSInfo[baseinfo]['cellId'] = int(body_info[begin_index + 6:begin_index + 14], 16)
            BSInfo[baseinfo]['cellId'] = int(body_info[begin_index + 6:begin_index + 14], 16)
            BSInfo[baseinfo]['mobileCountryCode'] = int(body_info[begin_index + 14:begin_index + 18], 16)
            BSInfo[baseinfo]['mobileNetworkCode'] = int(body_info[begin_index + 18:begin_index + 22], 16)
            BSInfo[baseinfo]['locationAreaCode'] = int(body_info[begin_index + 22:begin_index + 26], 16)
            BSInfo[baseinfo]['signalStrength'] = int(body_info[begin_index + 26:begin_index + 30], 16)
            begin_index += 30 - 2
        result['基站个数'] = BsInfocount
        result['基站信息'] = BSInfo
        return result, begin_index+2

    @run_on_executor
    def QueryCurActivationInfo(self, msg, id):
        try:
            body_info = msg[14:]
            CurActivationInfo = self.get_active_info(body_info)
            self.set_db_data(CurActivationInfo, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurActivationInfo error:%s' % e)

    def get_active_info(self, body_info):
        CurActivationInfo = {}
        CurActivationInfo['远程控制APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[0:2], 16))
        CurActivationInfo['SVT_APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[2:4], 16))
        CurActivationInfo['在线娱乐APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[4:6], 16))
        CurActivationInfo['旅途日志APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[6:8], 16))
        CurActivationInfo['车辆状态APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[8:10], 16))
        CurActivationInfo['iCall_APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[10:12], 16))
        CurActivationInfo['bCall_APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[12:14], 16))
        CurActivationInfo['Remote_Charge_APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[14:16], 16))
        CurActivationInfo['大数据APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[16:18], 16))
        CurActivationInfo['远程诊断APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[18:20], 16))
        CurActivationInfo['蓝牙钥匙APP激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[20:22], 16))
        return CurActivationInfo

    @run_on_executor
    def QueryCurIMSI(self, msg, id):
        try:
            body_info = msg[14:44]
            result = {'IMSI': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurIMSI error:%s' % e)

    @run_on_executor
    def QueryCurRoamingSetting(self, msg, id):
        try:
            body_info = Common.CommonVar.ROAMING_SETTING.get(int(msg[14:16],16))
            result = {'当前漫游设置': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurRoamingSetting error:%s' % e)


    @run_on_executor
    def QueryCurPrivacyModeSetting(self, msg, id):
        try:
            body_info = Common.CommonVar.PRIVACY_MODE.get(int(msg[14:16],16))
            result = {'当前用户私有数据搜集设置': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurPrivacyModeSetting error:%s' % e)

    @run_on_executor
    def QueryCurCSQ(self, msg, id):
        try:
            data = int(msg[14:16], 16)
            if data != 99:
                body_info = str(data)
            elif data == 99:
                body_info = SINGLE.get(99)
            result = {'当前信号强度': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurCSQ error:%s' % e)

    @run_on_executor
    def QueryCurBTKeyInfo(self, msg, id):
        try:
            body_info = msg[14:42]
            result = {'当前蓝牙钥匙信息': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurBTKeyInfo error:%s' % e)

    @run_on_executor
    def QueryCurMechKeyInfo(self, msg, id):
        try:
            body_info = msg[14:22]
            result = {'当前机械钥匙信息': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurMechKeyInfo error:%s' % e)


    @run_on_executor
    def QueryCurCallStatus(self, msg, id):
        try:
            body_info = Common.CommonVar.CALL_STATUE.get(int(msg[14:16],16))
            result = {'当前通话状态': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurCallStatus error:%s' % e)

    @run_on_executor
    def QueryCurToken(self, msg, id):
        try:
            body_info = msg[14:64+14]
            result = {'当前用户Token': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurToken error:%s' % e)

    @run_on_executor
    def QueryCurRoamingStatus(self, msg, id):
        try:
            body_info = Common.CommonVar.ROAMING_STATUE.get(int(msg[14:16],16))
            result = {'漫游状态': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurRoamingStatus error:%s' % e)

    @run_on_executor
    def QueryCurTBOXVERInfo(self, msg, id):
        try:
            body_info = msg[14:]
            result = {'TBOX版本信息': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            logger.info('QueryCurTBOXVERInfo error:%s' % e)

    @run_on_executor
    def QueryAllInfo(self,msg):
        #GPS信息
        gps_info = msg[14:358]
        result, end_index = self.get_gps(gps_info)
        self.set_db_data(result, 1, ' Communication.SocketClient.Executor      avnpara')
        #获取基站数
        basecount = msg[358:360]
        #获取基站信息
        basecount = 20
        baseinfo = msg[358:360+28*int(basecount)]
        baseInfo = self.get_bts(baseinfo)
        self.set_db_data(baseInfo[0], 2, 'avnpara')
        #获取激活信息
        avtiveafter = 360+28*int(basecount)
        active_msg = msg[avtiveafter:avtiveafter+22]
        db_content = self.get_active_info(active_msg)
        self.set_db_data(db_content, 3, 'avnpara')

        #获取wan信息
        wanafter = avtiveafter+22
        wan_status = msg[wanafter:wanafter + 32]
        db_content = self.get_wan(wan_status)
        self.set_db_data(db_content, 4, 'avnpara')

        #获取IMSI信息
        IMSI_after = wanafter + 32
        IMSI = msg[IMSI_after:IMSI_after + 30]
        self.set_db_data({'IMSI':IMSI}, 5, 'avnpara')


        #获取漫游信息
        RoamingAllowedafter = IMSI_after+30
        RoamingAllowed = msg[RoamingAllowedafter:RoamingAllowedafter + 2]
        body_info = Common.CommonVar.ROAMING_SETTING.get(int(RoamingAllowed, 16))
        result = {'当前漫游设置': body_info}
        self.set_db_data(result, 6, 'avnpara')

        #获取用户私有数据信息
        privacyafter = RoamingAllowedafter + 2
        RoamingAllowed = msg[privacyafter:privacyafter + 2]
        body_info = Common.CommonVar.PRIVACY_MODE.get(int(RoamingAllowed, 16))
        result = {'当前用户私有数据搜集设置': body_info}
        self.set_db_data(result, 7, 'avnpara')

        #获取信号信息
        singleafter = privacyafter + 2
        single = msg[singleafter:singleafter + 2]
        data = int(single, 16)
        if data < 10:
            body_info = SINGLE.get(10)
        elif data < 20:
            body_info = SINGLE.get(20)
        elif data < 32:
            body_info = SINGLE.get(30)
        elif data == 99:
            body_info = SINGLE.get(99)
        result = {'当前信号强度': body_info}
        self.set_db_data(result, 8, 'avnpara')

        #获取蓝牙解锁信息
        buleafter = singleafter +2
        body_info = msg[buleafter:buleafter+28]
        result = {'当前蓝牙钥匙信息': body_info}
        self.set_db_data(result, 9, 'avnpara')

        # 获取机械钥匙信息
        keyafter = buleafter+28
        body_info = msg[keyafter:keyafter+8]
        result = {'当前机械钥匙信息': body_info}
        self.set_db_data(result, 10, 'avnpara')

        # 获取通话状态信息
        callafter = keyafter+8
        call = msg[callafter:callafter+2]
        body_info = Common.CommonVar.CALL_STATUE.get(int(call))
        result = {'当前通话状态': body_info}
        self.set_db_data(result, 11, 'avnpara')


        # 获取用户token信息
        tokenafter = callafter+2
        db_content = {'当前用户Token': msg[tokenafter:tokenafter+64]}
        self.set_db_data(db_content, 12, 'avnpara')

        # 获取漫游状态信息
        roamingafter = tokenafter+64
        body_info = Common.CommonVar.ROAMING_STATUE.get(int(msg[roamingafter:roamingafter+2], 16))
        result = {'漫游状态': body_info}
        self.set_db_data(result, 13, 'avnpara')
        #ibox版本
        body_info = msg[roamingafter+2:]
        result = {'TBOX版本信息': body_info}
        self.set_db_data(result, 14, 'avnpara')


    def set_db_data(self, result, id, tablename=None ):
        try:
            session = Common.CommonVar.Session
            avn_gps = session.query(avn).filter_by(id=id).first()
            db_content = json.dumps(result, ensure_ascii=False)
            #if avn_gps.content != db_content:
            if 1:
                avn_gps.content = db_content
                avn_gps.count = int(avn_gps.count) + 1
                avn_gps.current = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                session.commit()
            # for key in result:
            #     avn_para = session.query(AvnPara.id).filter_by(parakey=key).first()
            #     if avn_para:
            #         avn_para = session.query(AvnPara).filter_by(parakey=key).first()
            #         if avn_para.paravalue != result.get(key):
            #             avn_para.current = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #             avn_para.paravalue = result.get(key)
            #             session.commit()
            #     else:
            #         if type(result.get(key)) is dict:
            #             data_dict = {key: '详细...'}
            #             self.insert_all_avn(tablename, data_dict, id)
            #             for child in result.get(key):
            #                 data_dict = {child: result.get(key).get(child)}
            #                 related_id = session.query(AvnPara.id).filter_by(parakey=key).first()[0]
            #                 self.insert_para_db(tablename, result.get(key).get(child), id, related_id, modify=False)
            #         else:
            #             data_dict = {key:result.get(key)}
            #             self.insert_all_avn(tablename, data_dict,id)

        except Exception as e:
            session.rollback()

    # def set_db_data2(self, result, id):
    #     try:
    #         session = Common.CommonVar.Session()
    #         avn_gps = session.query(avn).filter_by(id=id).first()
    #         db_content = json.dumps(result, ensure_ascii=False)
    #         if avn_gps.content != db_content:
    #             avn_gps.content = db_content
    #             avn_gps.count = int(avn_gps.count) + 1
    #             avn_gps.current = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #             session.commit()
    #         for key in result:
    #             avn_para = session.query(AvnPara).filter_by(parakey=key).first()
    #             if avn_para.paravalue != result.get(key):
    #                 avn_para.current = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #                 avn_para.paravalue = result.get(key)
    #                 session.commit()
    #
    #     except Exception as e:
    #         session.rollback()

    def insert_all_avn(self, table_name, data_dict,id , modify=True):
        if modify:
            pd_dict = self.modify_dataFrame(data_dict, id)
        else:
            pd_dict = data_dict
        df = pd.DataFrame(pd_dict)
        # 第一种插入方法(pandas to_sql)
        # 在使用to_sql时注意if_exists参数，如果是replace的话它会先drop掉表，然后再创建表，最后插入数据
        df.to_sql(table_name, con=Common.CommonVar.ENGINE, if_exists='append', index=False)

    def insert_para_db(self, table_name, data_dict,id ,related_id, modify=True):
        for para in data_dict:
            data = {para:data_dict.get(para)}
            data_dict = self.modify_child_dataFrame(data, id, related_id)
            self.insert_all_avn(table_name, data,id , modify)



    def modify_dataFrame(self, data_dict,id):
        pd_dict = {}
        pd_dict['parakey'] = list(data_dict.keys())
        pd_dict['paravalue'] = list(data_dict.values())
        current = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pd_dict['current'] = [current]*len(data_dict)
        pd_dict['creatime'] = [current] * len(data_dict)
        pd_dict['_locked'] = [0] * len(data_dict)
        pd_dict['related_avn_id'] = [id] * len(data_dict)
        return pd_dict

    def modify_child_dataFrame(self, data_dict,id, related_id):
        pd_dict = {}
        pd_dict['parakey'] = list(data_dict.keys())
        pd_dict['paravalue'] = list(data_dict.values())
        current = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pd_dict['current'] = [current]*len(data_dict)
        pd_dict['creatime'] = [current] * len(data_dict)
        pd_dict['_locked'] = [0] * len(data_dict)
        pd_dict['related_avn_id'] = [id] * len(data_dict)
        pd_dict['related_para_id'] = [related_id] * len(data_dict)
        return pd_dict



    def handle_sendmsg(self, cmdWord, msg,**kwargs):
        msg_header = None
        if msg is not None:
            #接收到消息后的处理
            ctrlByte = msg[10:12]
            if ctrlByte != '00':
                if cmdWord == '0104' or cmdWord == '0304':
                    self.QueryCurWANConnInfo(msg, 4)
                elif cmdWord == '0101':
                    self.QueryCurGPSInfo(msg,1)
                elif cmdWord == '0102':
                    self.QueryCurBSInfo(msg,2)
                elif cmdWord == '0103':
                    self.QueryCurActivationInfo(msg,3)
                elif cmdWord == '0105' or cmdWord == '0305':
                    self.QueryCurIMSI(msg, 5)
                    pass
                elif cmdWord == '0106' or cmdWord == '0306':
                    self.QueryCurRoamingSetting(msg, 6)
                elif cmdWord == '0107' or cmdWord == '0307':
                    self.QueryCurPrivacyModeSetting(msg, 7)
                elif cmdWord == '0108' or cmdWord == '0308':
                    self.QueryCurCSQ(msg, 8)
                elif cmdWord == '0109' or cmdWord == '0309':
                    self.QueryCurBTKeyInfo(msg, 9)
                elif cmdWord == '010a' :
                    self.QueryCurMechKeyInfo(msg, 10)
                elif cmdWord == '010b' or cmdWord == '030b':
                    self.QueryCurCallStatus(msg, 11)
                elif cmdWord == '010c' or cmdWord == '030c':
                    self.QueryCurToken(msg, 12)
                elif cmdWord == '010d'or cmdWord == '030d':
                    self.QueryCurRoamingStatus(msg, 13)
                elif cmdWord == '010f':
                    self.QueryCurTBOXVERInfo(msg, 14)
                elif cmdWord == '0100' :
                    self.QueryAllInfo(msg)
                elif cmdWord == '0002':
                    self.Timing_send('0002')
                elif cmdWord == '0315':
                    self.sendMsg('0315')


                return None
            # elif ctrlByte != '00' and cmdWord == '0001':
            #     msg_header = '81080000010001'
        if not msg_header:
            # 发送的处理
            if cmdWord == '0001':
                msg_header = '81080001000001'
            elif cmdWord == '0000':
                msg_header = '81080000000001'
            elif cmdWord == '0008':
                msg_header = '81080008000001'
            elif cmdWord == 'ffff':
                msg_header = '810800ffff0001'
            elif cmdWord == '0002':
                msg_header = '81080002000001'
            elif cmdWord == '0100':
                msg_header = '81080000010001'
            elif cmdWord == '0101':
                msg_header = '81080001010001'

            elif cmdWord == '0102':
                msg_header = '8108000201000'
            elif cmdWord == '0103':
                msg_header = '81080003010001'
            elif cmdWord == '0104':
                msg_header = '81080004010001'
            elif cmdWord == '0105':
                msg_header = '81080005010001'
                # msg_header = '00000000000000'
            elif cmdWord == '0106':
                msg_header = '81080006010001'
            elif cmdWord == '0107':
                msg_header = '81080007010001'
            elif cmdWord == '0108':
                msg_header = '81080008010001'
            elif cmdWord == '0109':
                msg_header = '81080009010001'
            elif cmdWord == '010a':
                msg_header = '8108000a010001'
            elif cmdWord == '010b':
                msg_header = '8108000b010001'
            elif cmdWord == '010c':
                msg_header = '8108000c010001'
            elif cmdWord == '010d':
                msg_header = '8108000d010001'
            elif cmdWord == '010f':
                msg_header = '8108000f010001'
            elif cmdWord == '0201':
                result = self.db_session.query(avn.content).filter_by(id=6).first()
                curr_set = eval(result[0]).get('当前漫游设置')
                if curr_set == '不允许漫游':
                    msg_header = '8109000102000101'
                else:
                    msg_header = '8109000102000100'
            elif cmdWord == '0202':
                result = self.db_session.query(avn.content).filter_by(id=7).first()
                curr_set = eval(result[0]).get('当前用户私有数据搜集设置')
                if curr_set == '不允许搜集用户私有数据':
                    msg_header = '8109000202000101'
                else:
                    msg_header = '8109000202000100'
            elif cmdWord == '0203':
                CallType = kwargs.get('CallType').zfill(2)
                CallCenterID = kwargs.get('CallCenterID').zfill(2)
                msg_header = '810A0003020001'+CallType+CallCenterID
            elif cmdWord == '0204':
                msg_header = '81080004020001'
            elif cmdWord == '0205':
                msg_header = '81080005020001'
            elif cmdWord == '0206':
                msg_header = '81080006020001'
            elif cmdWord == '0207':
                para = kwargs.get('DataValue').zfill(2)
                msg_header = '81090007020001' + para
            elif cmdWord == '0208':
                ex_ECU_ID = kwargs.get('ex_ECU_ID').zfill(2)
                ReflashReqInfo = kwargs.get('ReflashReqInfo').zfill(2)
                msg_header = '81090008020001' + ex_ECU_ID + ReflashReqInfo
            elif cmdWord == '0209':
                reset_value = kwargs.get('reset_value')
                if int(reset_value) ==1:
                    msg_header = '8109000902000101'
                elif int(reset_value) ==2:
                    msg_header = '8109000902000102'
                elif int(reset_value) ==3:
                    msg_header = '8109000902000103'
                else:
                    raise

            elif cmdWord == '020d':
                ECU_ID = kwargs.get('ECU_ID').zfill(2)
                DATE = self.set_date(kwargs.get('DATE'))
                str_date = DATE[2:].zfill(8)
                msg_header = '8109000d020001' + ECU_ID +str_date[6:8]+ str_date[4:6]+str_date[2:4]+ str_date[0:2]
            elif cmdWord == '0301':
                msg_header = '81080001030101'
                self.QueryCurGPSInfo(msg, 1)
            elif cmdWord == '0302':
                msg_header = '81080002030101'
                self.QueryCurBSInfo(msg,2)
            elif cmdWord == '0303':
                msg_header = '81080003030101'
                self.QueryCurActivationInfo(msg,3)
            elif cmdWord == '0304':
                msg_header = '81080004030101'
                self.QueryCurWANConnInfo(msg, 4)
            elif cmdWord == '0305':
                pass
                msg_header = '81080005030101'
                self.QueryCurIMSI(msg, 5)
            elif cmdWord == '0306':
                    self.QueryCurRoamingSetting(msg, 6)
                    msg_header = '81080006030001'
            elif cmdWord == '0307':
                    self.QueryCurRoamingSetting(msg, 6)
                    msg_header = '81080007030001'
            elif cmdWord == '0308':
                msg_header = '81080008030101'
                self.QueryCurCSQ(msg, 8)
            elif cmdWord == '0309':
                msg_header = '81080009030101'
                self.QueryCurBTKeyInfo(msg, 9)
            elif cmdWord == '030b':
                msg_header = '8108000b030101'
                self.QueryCurCallStatus(msg, 11)
            elif cmdWord == '030c':
                msg_header = '8108000c030101'
                self.QueryCurToken(msg, 12)
            elif cmdWord == '030d':
                msg_header = '8108000d030101'
                self.QueryCurRoamingStatus(msg, 13)
            elif cmdWord == '030e':
                msg_header = '8108000e030101'
                self.QueryCurRoamingStatus(msg, 13)
            elif cmdWord == '030e':
                msg_header = '8108000e030401'
            elif cmdWord == '030f':
                #self.QueryCurTBOXVERInfo(msg, 14)
                msg_header = '8108000f030101'
            elif cmdWord == '0310':
                msg_header = '81080010030101'
            elif cmdWord == '0311':
                msg_header = '81080011030101'
            elif cmdWord == '0313':
                msg_header = '81080013030101'
            elif cmdWord == '0314':
                msg_header = '81080014030101'
            elif cmdWord == '0315':
                msg_header = '81080015030101'
            elif cmdWord == '0401':
                msg_header = '81080001040101'
            elif cmdWord == '0501':
                msg_header = '81080001050101'
            elif cmdWord == '0502':
                msg_header = '81080002050101'
            elif cmdWord == '0505':
                msg_header = '81080005050101'
            elif cmdWord == '0506':
                msg_header = '81080006050101'
            elif cmdWord == '0507':
                msg_header = '81080007050101'
            elif cmdWord == '0000':
                pass
            elif cmdWord == '0003':
                msg_header = '81080003000001'
            else:
                pass
        if msg_header:
            msg_header_lst = []
            for i in range(int(len(msg_header) / 2)):
                msg_header_lst.append(msg_header[2 * i:2 * (i + 1)])
            msg_tail = int(msg_header_lst[0], 16)
            for i in range(1, len(msg_header_lst)):
                msg_tail = msg_tail ^ int(msg_header_lst[i], 16)
            msg_tail = hex(msg_tail)[2:]
            if len(msg_tail) < 2:
                msg_tail = '0' + msg_tail
            # msg_tail = 'ff'
            msg = msg_header + msg_tail
            if cmdWord in self.nosendlist:
                return None
            return unhexlify(msg)
        else:
            return None

    @run_on_executor
    def Timing_send(self, cmd):
        while 1:
            self.sendMsg(cmd)
            time.sleep(1)

    def set_date(self, datestr):

        timeDateStr = datestr
        time1 = datetime.datetime.strptime(timeDateStr, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime('1970-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        return str(hex(int((time1-time2).total_seconds())))
    @staticmethod
    def get_instances(host, port):
        if (host, port) not in USBIAgree.instancesobj:
            USBIAgree.instancesobj[(host, port)] = USBIAgree(host, port)
        return USBIAgree.instancesobj[(host, port)]
