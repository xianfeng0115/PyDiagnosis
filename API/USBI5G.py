# coding:utf-8

import os
from Communication.SocketClient import BaseClient
from Common.CommonVar import logger,SINGLE
from Common.CommonFun import *
from binascii import hexlify, unhexlify
import time, datetime
try:
    from DB.avn_table import AvnSimu5G as avn
except:
    from create_db import make_db
    make_db()
    from DB.avn_table import AvnSimu5G as avn
    pass

#from DB.avn_table import AvnPara
import Common.CommonVar
import binascii
import json
from tornado.concurrent import run_on_executor
from tornado import ioloop, gen, iostream
from concurrent.futures import ThreadPoolExecutor
import socket
import queue
import tarfile
import gzip

import pandas as pd
from API.Logger import Loggers
from API.Py_excle import *
from io import StringIO
import asyncio
import sys
import tornado

class USBIAgree5G(BaseClient):
    executor = ThreadPoolExecutor(100)
    def __init__(self, host, port):
        BaseClient.__init__(self, host, port)
        self.t1 = None
        self.host = host
        self.port = port
        self.heart_flag = 1
        self.result_flag = 0
        self.result_dict = {}
        if 'root_path' in os.environ:
            rootpath = os.environ['root_path']
        else:
            rootpath = os.path.dirname(os.path.abspath(__file__))
        self.logpath = os.path.join(rootpath, 'Log')
        cfg = pyExcel.get_instances()
        self.logger = Loggers.get_instances(filename='avn_5g.log', log_dir=self.logpath,
                                            logtype=cfg.get_cfgkey_value('avn_logtype'))
        self.db_session = Common.CommonVar.Session()
        self.nosendlist = []
        self.reset_para = ''
        self.log = b''
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.ioloop = tornado.ioloop.IOLoop.instance()

    def decode(self, str):
        if type(str) is bytes:
            return str.decode("ISO-8859-1")
        return str

    def encode(self, str):
        if type(str) is not bytes:
            try:
                return str.encode("ISO-8859-1")
            except:
                return str
        return str

    def start_tornado(self):
        self.ioloop.start()

    def loginApi(self):
        if not self.t1:
            self.t1 = Thread(target=self.start_tornado)
            self.t1.setDaemon(True)
            self.t1.start()

        self.ioloop.spawn_callback(self.connect_socket)
        # simu.connect_socket()
        time.sleep(5)
        self.sendMsg('0001')

    def USBI_close(self):
        self.handle_close()


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
            self.logger.info('QueryCurWANConnInfo error:%s'%e)

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
             self.logger.info('QueryCurGPSInfo error:%s'%e)



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
            self.logger.info('QueryCurBSInfo error:%s' % e)

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
            self.logger.info('QueryCurActivationInfo error:%s' % e)

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
        CurActivationInfo['5G网络激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[22:24], 16))
        CurActivationInfo['iBOX 5G网络激活状态'] = Common.CommonVar.ACTIVE_STATUE.get(int(body_info[24:26], 16))
        return CurActivationInfo

    @run_on_executor
    def QueryCurIMSI(self, msg, id):
        try:
            body_info = msg[14:44]
            result = {'IMSI': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurIMSI error:%s' % e)

    @run_on_executor
    def QueryCurRoamingSetting(self, msg, id):
        try:
            body_info = Common.CommonVar.ROAMING_SETTING.get(int(msg[14:16],16))
            result = {'当前漫游设置': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurRoamingSetting error:%s' % e)


    @run_on_executor
    def QueryCurPrivacyModeSetting(self, msg, id):
        try:
            body_info = Common.CommonVar.PRIVACY_MODE.get(int(msg[14:16], 16))
            result = {'当前用户私有数据搜集设置': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurPrivacyModeSetting error:%s' % e)

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
            self.logger.info('QueryCurCSQ error:%s' % e)

    @run_on_executor
    def QueryCurBTKeyInfo(self, msg, id):
        try:
            body_info = msg[14:42]
            result = {'当前蓝牙钥匙信息': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurBTKeyInfo error:%s' % e)

    @run_on_executor
    def QueryCurMechKeyInfo(self, msg, id):
        try:
            body_info = msg[14:22]
            result = {'当前机械钥匙信息': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurMechKeyInfo error:%s' % e)


    @run_on_executor
    def QueryCurCallStatus(self, msg, id):
        try:
            body_info = Common.CommonVar.CALL_STATUE.get(int(msg[14:16],16))
            result = {'当前通话状态': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurCallStatus error:%s' % e)

    @run_on_executor
    def QueryCurToken(self, msg, id):
        try:
            body_info = msg[14:64+14]
            result = {'当前用户Token': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurToken error:%s' % e)

    @run_on_executor
    def QueryCurRoamingStatus(self, msg, id):
        try:
            body_info = Common.CommonVar.ROAMING_STATUE.get(int(msg[14:16],16))
            result = {'漫游状态': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurRoamingStatus error:%s' % e)

    @run_on_executor
    def QueryRemoteReflashCheckUpdate(self, msg, id):
        try:
            body_info = Common.CommonVar.RemoteReflashCheckUpdate['Status'].get(msg[14:16])
            result = {'Status': body_info}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurRoamingStatus error:%s' % e)

    @run_on_executor
    def QueryRemoteDownloadStatusUpdate(self, msg, id):
        try:
            Status = Common.CommonVar.RemoteDownloadStatusUpdate['Status'].get(int(msg[14:16], 16))
            ECUID = Common.CommonVar.RemoteDownloadStatusUpdate['ECUID'].get(int(msg[16:18], 16))
            NumOfEcus = int(msg[18:20], 16)
            FailReason = Common.CommonVar.RemoteDownloadStatusUpdate['FailReason'].get(int(msg[20:22], 16))
            result = {'Status': Status, 'ECUID':ECUID, 'NumOfEcus':NumOfEcus, 'FailReason':FailReason}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurRoamingStatus error:%s' % e)

        @run_on_executor
        def QueryRemoteReflashStatusUpdate(self, msg, id):
            try:
                Status = Common.CommonVar.RemoteReflashStatusUpdate['Status'].get(int(msg[14:16], 16))
                ECU_TYPE = Common.CommonVar.RemoteReflashStatusUpdate['ECU_TYPE'].get(msg[16:18])
                ECUID  = Common.CommonVar.RemoteReflashStatusUpdate['ECUID'].get(int(msg[18:20], 16))
                Percentage = int(msg[20:22], 16)
                NumOfEcus = int(msg[22:24], 16)
                NumLeft = int(msg[24:26], 16)
                FailReason = Common.CommonVar.RemoteReflashStatusUpdate['FailReason'].get(int(msg[26:28], 16))
                result = {'Status': Status,'ECU_TYPE':ECU_TYPE,'Percentage':Percentage,'NumLeft':NumLeft,  'ECUID': ECUID, 'NumOfEcus': NumOfEcus, 'FailReason': FailReason}
                self.set_db_data(result, id, 'avnpara')
            except Exception as e:
                self.logger.info('QueryCurRoamingStatus error:%s' % e)

        @run_on_executor
        def QueryRemoteReflashTips(self, msg, id):
            try:
                TipsInfo = unhexlify(self.encode(msg[14:]))
                result = {'TipsInfo':  TipsInfo}
                self.set_db_data(result, id, 'avnpara')
            except Exception as e:
                self.logger.info('QueryCurRoamingStatus error:%s' % e)

        @run_on_executor
        def QueryAVNReflashModePermission(self, msg, id):
            try:
                EnterPermission  = Common.CommonVar.AVNReflashModePermission['ECUID'].get(int(msg[14:16], 16))
                result = {'EnterPermission':  EnterPermission}
                self.set_db_data(result, id, 'avnpara')
            except Exception as e:
                self.logger.info('QueryCurRoamingStatus error:%s' % e)

        @run_on_executor
        def QueryQueryRemoteReflashDetail(self, msg, id):
            try:
                NumOfPkgs   = int(msg[14:16], 16)
                PackageInfo = unhexlify(self.encode(msg[16:-2]))
                CHARGE_FLAG = Common.CommonVar.RemoteReflashDetail['CHARGE_FLAG'].get(int(msg[-2:], 16))
                result = {'NumOfPkgs':  NumOfPkgs, 'PackageInfo':PackageInfo, 'CHARGE_FLAG':CHARGE_FLAG}
                self.set_db_data(result, id, 'avnpara')
            except Exception as e:
                self.logger.info('QueryCurRoamingStatus error:%s' % e)

        @run_on_executor
        def QueryRemoteReflashInform(self, msg, id):
            try:
                ReflashReqInfo = Common.CommonVar.RemoteReflashInform['ReflashReqInfo'].get(int(msg[14:16], 16))
                ECU_TYPE = Common.CommonVar.RemoteReflashInform['ECU_TYPE'].get(msg[16:18], 16)
                result = {'ReflashReqInfo':  ReflashReqInfo,'ECU_TYPE':ECU_TYPE}
                self.set_db_data(result, id, 'avnpara')
            except Exception as e:
                self.logger.info('QueryCurRoamingStatus error:%s' % e)


    @run_on_executor
    def QueryRemoteReflashCheckUpdate(self, msg, id):
        try:
            Status = Common.CommonVar.RemoteReflashCheckUpdate['Status'].get(msg[14:16])
            result = {'Status': Status}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurRoamingStatus error:%s' % e)

    @run_on_executor
    def QueryCurTBOXVERInfo(self, msg, id):
        try:
            body_info = msg[14:]
            MCU_LEN = body_info[:2]
            MCU_VER = body_info[2:130]
            MPU_LEN = body_info[130:132]
            MPU_VER = body_info[132:260]
            MODEM_LEN = body_info[260:262]
            MODEM_VER = body_info[262:390]
            BT_LEN = body_info[390:392]
            BT_VER = body_info[392:520]
            MCU_VER = self.to_ascii(MCU_VER).strip('\x00')
            MPU_VER = self.to_ascii(MPU_VER).strip('\x00')
            MODEM_VER = self.to_ascii(MODEM_VER).strip('\x00')
            if BT_VER:
                BT_VER = self.to_ascii(BT_VER).strip('\x00')
            else:
                BT_VER = ''

            result = {'MCU_VER': MCU_VER, 'MPU_VER':MPU_VER, 'MODEM_VER':MODEM_VER, 'BT_VER':BT_VER}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurTBOXVERInfo error:%s' % e)

    def to_ascii(self,h):
        list_s = []
        for i in range(0, len(h), 2):
            list_s.append(chr(int(h[i:i+2], 16)))
        return ''.join(list_s)

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
        MCU_LEN = body_info[:2]
        MCU_VER = body_info[2:130]
        MPU_LEN = body_info[130:132]
        MPU_VER = body_info[132:260]
        MODEM_LEN = body_info[260:262]
        MODEM_VER = body_info[262:390]
        BT_LEN = body_info[390:392]
        BT_VER = body_info[392:520]
        MCU_VER = self.to_ascii(MCU_VER).strip('\x00')
        MPU_VER = self.to_ascii(MPU_VER).strip('\x00')
        MODEM_VER = self.to_ascii(MODEM_VER).strip('\x00')
        BT_VER = self.to_ascii(BT_VER).strip('\x00')

        result = {'MCU_VER': MCU_VER, 'MPU_VER': MPU_VER, 'MODEM_VER': MODEM_VER, 'BT_VER': BT_VER}
        self.set_db_data(result, 14, 'avnpara')

    def get_db_data(self, id):
        try:
            session = Common.CommonVar.Session
            avn_gps = session.query(avn).filter_by(id=id).first()
            return avn_gps.to_json()
        except:
            self.logger.info('get_db_data error ')

    def set_db_data(self, result, id, tablename=None ):
        try:
            session = Common.CommonVar.Session
            avn_gps = session.query(avn).filter_by(id=id).first()
            try:
                db_content = json.dumps(result, ensure_ascii=False)
            except:
                db_content = {result}
            # db_content = avn_gps.to_json()
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


    @run_on_executor
    def QueryFunctionStatus(self,msg, id):
        body_info = Common.CommonVar.ROAMING_STATUE.get(int(msg[14:16], 16))
        result = {'v2xStatus': body_info}
        self.set_db_data(result, id, 'avnpara')

    @run_on_executor
    def QueryRoadInformation(self,msg, id):
        RoadInfo01 = '无标识' if int(msg[14:16], 16) == 0 else int(msg[14:16], 16)
        RoadInfo02 = '无标识' if int(msg[16:18], 16) == 0 else int(msg[16:18], 16)
        RoadInfo03 = Common.CommonVar.RoadInformation.get('RoadInfo03').get(int(msg[18:20], 16))
        RoadInfo04 = '无标识' if int(msg[20:22], 16) == 0 else int(msg[20:22], 16)
        RoadInfo05 = Common.CommonVar.RoadInformation.get('RoadInfo03').get(int(msg[22:24], 16))
        RoadInfo06 = '无标识' if int(msg[24:26], 16) == 0 else int(msg[24:26], 16)
        RoadInfo07 = '无标识' if int(msg[26:28], 16) == 0 else '施工路段标识下发'
        RoadInfo08 = '无标识' if int(msg[28:30], 16) == 0 else int(msg[28:30], 16)
        RoadInfo09 = Common.CommonVar.RoadInformation.get('RoadInfo09').get(int(msg[30:32], 16))
        RoadInfo10 = '无标识' if int(msg[32:34], 16) == 0 else int(msg[32:34], 16)

        result = {'限速（Km/h）': RoadInfo01, '限速距离（m）':RoadInfo02,
                  '弯道':RoadInfo03, '弯道距离（m）':RoadInfo04,
                   '减速区':RoadInfo05,'减速区距离（m）':RoadInfo06,
                  '施工路段':RoadInfo07,'施工路段距离（m）':RoadInfo08,
                  '关键路段':RoadInfo09,'建议车速（Km/h）':RoadInfo10
                  }
        self.set_db_data(result, id, 'avnpara')


    @run_on_executor
    def getwifiinfo(self,msg, id):
        ReWifiInfo = unhexlify(self.encode(msg[14:46]))
        ReWifiInfo2 =  'Wifi打开' if int(msg[46:48], 16) else 'Wifi关闭'
        ReWifiInfo3 =unhexlify(self.encode(msg[48:68]))
        ReWifiInfo4 = '2.4G频段和5G频段' if int(msg[46:48], 16) == 1  else '5G频段'
        result = {'本机名称': ReWifiInfo,'Wifi开关':ReWifiInfo2, '热点密码':ReWifiInfo3,'频段':ReWifiInfo4}
        self.set_db_data(result, id, 'avnpara')

    @run_on_executor
    def getwifilist(self,msg, id):
        index = 14
        result = {}
        while 1:
            if len(msg[14:]) < index+64:
                break
            else:
                ReWifiInfo = unhexlify(self.encode(msg[index:index+64]))
                result['设备'] = ReWifiInfo
                index += 64

        self.set_db_data(result, id, 'avnpara')

    @run_on_executor
    def getsn(self,msg, id):
        ReWifiInfo = decode(unhexlify(self.encode(msg[14:44])))
        ReWifiInfo2= decode(unhexlify(self.encode(msg[44:68])))
        ReWifiInfo3 =decode(unhexlify(self.encode(msg[68:108])))[4:]
        result = {'IMSI': ReWifiInfo,'iBOXSN':ReWifiInfo2, 'ICCID':ReWifiInfo3}
        self.set_db_data(result, id, 'avnpara')

    def handle_sendmsg(self, cmdWord, msg,**kwargs):
        msg_header = None
        if msg is not None:
            #1为响应包
            ctrlByte = msg[10:12]

            if ctrlByte == '01':
                if self.result_flag:
                    self.result_dict[cmdWord] = [msg, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')]
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
                elif cmdWord == '010a':
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

                    if self.heart_flag:
                        self.sendMsg('0002')
                elif cmdWord == '0315':
                    self.sendMsg('0315')

                elif cmdWord == '0312':
                    self.QueryRemoteReflashTips(msg, 18)
                elif cmdWord == '0313':
                    self.QueryAVNReflashModePermission(msg, 19)
                elif cmdWord == '0314':
                    self.QueryRemoteReflashDetail(msg, 20)
                elif cmdWord == '0315':
                    self.QueryRemoteReflashInform(msg, 21)
                elif cmdWord == '0007':
                    self.QueryFunctionStatus(msg, 23)

                elif cmdWord == '0005':
                    self.QueryRoadInformation(msg, 24)


                elif cmdWord == '0111':
                    self.getwifiinfo(msg, 25)
                elif cmdWord == '0112':
                    self.getwifilist(msg, 26)
                elif cmdWord == '0113':
                    self.getsn(msg, 27)

                elif cmdWord == '0320':
                    msg_header = '810800000020030101'

                elif cmdWord == '0203':
                    self.result_dict[cmdWord] = msg
                elif cmdWord == '0204':
                    self.result_dict[cmdWord] = msg
                elif cmdWord == '0205':
                    self.result_dict[cmdWord] = msg
                elif cmdWord == '0206':
                    self.result_dict[cmdWord] = msg
                elif cmdWord == '0207':
                    self.result_dict[cmdWord] = msg
                return None
            # elif ctrlByte != '00' and cmdWord == '0001':
            #     msg_header = '81080000010001'
        if not msg_header:
            # 发送的处理
            if cmdWord == '0001':
                msg_header = '81080001000001'
            elif cmdWord == '0000':
                msg_header = '81080000000001'
            elif cmdWord == '0007':
                msg_header = '81080007000001'
            elif cmdWord == '0005':
                msg_header = '81080005000001'
            elif cmdWord == '0110':
                msg_header = '81080010010001' + str(kwargs.get('RemoteGetLog')).zfill(2)

            elif cmdWord == '0111':
                msg_header = '81080011010001'

            elif cmdWord == '0112':
                msg_header = '81080012010001'
            elif cmdWord == '0113':
                msg_header = '81080013010001'

            elif cmdWord == '0008':
                msg_header = '81080007000001'
            elif cmdWord == 'ffff':
                msg_header = '810800ffff0001'
            elif cmdWord == '0002':
                msg_header = '81080002000001'
            elif cmdWord == '0100':
                msg_header = '81080000010001'
            elif cmdWord == '0101':
                msg_header = '81080001010001'

            elif cmdWord == '0102':
                msg_header = '81080002010001'
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
            elif cmdWord == '020e':
                wifiFlag = kwargs.get('wifiFlag').zfill(2)
                wifipwd = hexlify(kwargs.get('wifipwd')).zfill(20)
                wifiFrequency = kwargs.get('wifiFrequency').zfill(2)
                msg_header = '8109000e020001' + wifiFlag + wifipwd + wifiFrequency

            elif cmdWord == '020f':
                EnableInfo = kwargs.get('EnableInfo').zfill(2)
                msg_header = '8109000f020001' + EnableInfo

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
                    body = msg[14:16]
                    msg_header = '81080006030101' + body
            elif cmdWord == '0307':
                    self.QueryCurRoamingSetting(msg, 6)
                    msg_header = '81080007030101'
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
                self.QueryRemoteReflashCheckUpdate(msg, 15)
                msg_header = '8108000f030101'
            elif cmdWord == '0310':
                self.QueryRemoteDownloadStatusUpdate(msg, 16)
                msg_header = '81080010030101'
            elif cmdWord == '0311':
                self.QueryRemoteReflashStatusUpdate(msg, 17)
                msg_header = '81080011030101'
            elif cmdWord == '0312':
                self.QueryRemoteReflashTips(msg, 18)
                msg_header = '81080012030101'
            elif cmdWord == '0313':
                self.QueryAVNReflashModePermission(msg, 19)
                msg_header = '81080013030101'
            elif cmdWord == '0314':
                self.QueryRemoteReflashDetail(msg, 20)
                msg_header = '81080014030101'
            elif cmdWord == '0315':
                self.QueryRemoteReflashInform(msg, 21)
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
                msg_header = '81080003000101'
            elif cmdWord == '0320':
                msg_header = '810800000020030101'
                pass
            else:
                pass
        if msg_header:
            msg_header = self.modify_len(msg_header)
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
    def QueryAVNReflashModePermission(self, msg, id):
        try:
            EnterPermission  = Common.CommonVar.AVNReflashModePermission['EnterPermission'].get(int(msg[14:16], 16))
            result = {'EnterPermission':  EnterPermission}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('AVNReflashModePermission error:%s' % e)

    @run_on_executor
    def QueryRemoteReflashDetail(self, msg, id):
        try:
            NumOfPkgs   = int(msg[14:16], 16)
            ECU = int(msg[16:18], 16)
            UPDATE_TIME = int(msg[18:20], 16)
            ECU_TYPE = Common.CommonVar.RemoteReflashInform['ECU_TYPE'].get(msg[20:22], 16)
            VER_DESC = unhexlify(self.encode(msg[22:24]))
            VER_DESC_LENGTH = int(msg[24:26], 16)
            CHARGE_FLAG = Common.CommonVar.RemoteReflashDetail['CHARGE_FLAG'].get(int(msg[-2:], 16))
            result = {'NumOfPkgs':  ECU, 'PackageInfo':ECU,'UPDATE_TIME':UPDATE_TIME,
                      'ECU_TYPE':ECU_TYPE,'VER_DESC':VER_DESC,'VER_DESC_LENGTH':VER_DESC_LENGTH,
                      'CHARGE_FLAG':CHARGE_FLAG}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurRoamingStatus error:%s' % e)

    @run_on_executor
    def QueryRemoteReflashStatusUpdate(self, msg, id):
        try:
            Status = Common.CommonVar.RemoteReflashStatusUpdate['Status'].get(int(msg[14:16], 16))
            ECU_TYPE = Common.CommonVar.RemoteReflashStatusUpdate['ECU_TYPE'].get(msg[16:18])
            ECUID  = Common.CommonVar.RemoteReflashStatusUpdate['ECUID'].get(int(msg[18:20], 16))
            Percentage = int(msg[20:22], 16)
            NumOfEcus = int(msg[22:24], 16)
            NumLeft = int(msg[24:26], 16)
            FailReason = Common.CommonVar.RemoteReflashStatusUpdate['FailReason'].get(int(msg[26:28], 16))
            result = {'Status': Status,'ECU_TYPE':ECU_TYPE,'Percentage':Percentage,'NumLeft':NumLeft,  'ECUID': ECUID, 'NumOfEcus': NumOfEcus, 'FailReason': FailReason}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurRoamingStatus error:%s' % e)

    @run_on_executor
    def QueryRemoteReflashTips(self, msg, id):
        try:
            TipsInfo = unhexlify(self.encode(msg[14:]))
            result = {'TipsInfo':  TipsInfo}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurRoamingStatus error:%s' % e)



    @run_on_executor
    def QueryRemoteReflashInform(self, msg, id):
        try:
            ReflashReqInfo = Common.CommonVar.RemoteReflashInform['ReflashReqInfo'].get(int(msg[14:16], 16))
            ECU_TYPE = Common.CommonVar.RemoteReflashInform['ECU_TYPE'].get(msg[16:18], 16)
            result = {'ReflashReqInfo':  ReflashReqInfo,'ECU_TYPE':ECU_TYPE}
            self.set_db_data(result, id, 'avnpara')
        except Exception as e:
            self.logger.info('QueryCurRoamingStatus error:%s' % e)


    def modify_len(self, msg):
        msgFalg = msg[:2]
        msgdetil = msg[4:]
        msg_len = hex((len(msg)+2)//2)[2:].zfill(2)
        return msgFalg + msg_len + msgdetil

    # @run_on_executor
    @asyncfun
    def Timing_send(self, cmd):
        while 1:
            self.sendMsg(cmd)
            time.sleep(1)

    def set_date(self, datestr):

        timeDateStr = datestr
        time1 = datetime.datetime.strptime(timeDateStr, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime('1970-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        return str(hex(int((time1-time2).total_seconds())))

    @run_on_executor
    def getLog(self, avn_cmd):
        try:
            result={'状态':'下载开始'}
            self.set_db_data(result, 28, 'avnpara')
            log_channel = USBIAgree5G(self.host, int(self.port)+1)
            Common.CommonVar.loop.spawn_callback(log_channel.connect_socket_log)
            # log_channel.sendMsg('0320')
        except Exception as e:
            self.logger.info('getLog error:%s' % e)

    async def connect_socket_log(self):
            self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            self.session = iostream.IOStream(self.sock_fd)
            await self.session.connect((self.host, int(self.port)))
            await self.mornitinglog()


            # self.session = TCPClient()
            # self.session.connect(self.host, self.port, self.morniting)

            # yield self.morniting()

    async def mornitinglog(self):
        while self.closeFlag:
            try:
                sendMsg = b''
                msg = await self.session.read_bytes(32768, partial=True)
                Msg = hexlify(msg)
                cmd = decode(self.encode(Msg[12:14] + Msg[10:12]))
                self.logger.info('接受数据%s,CMD:%s' % (Msg, cmd))
                head = decode(self.encode(Msg[:2]))
                # sendMsg = self.handle_sendmsg(decode(cmd), decode(hexlify(msg)))
                if head =='18' and cmd == '0320':

                    sendMsg = unhexlify(self.encode(Msg)[:14] + b'0101')
                elif head !='18' and  '2103' in decode(Msg)[-18:] and '18' in decode(Msg)[-18:] :
                    self.logger.info('log is %s, size is %s' % (decode(hexlify(self.log)), len(hexlify(self.log))/2))
                    sendMsg = unhexlify(self.encode(decode(Msg)[-18:][:14]) + b'0101')
                    self.session.write(sendMsg)
                    self.log += msg
                    loginfo = self.log[:-18]
                    logpath = os.path.join(os.environ['root_path'], 'Log','ibox.tar.gz')
                    with open(logpath, 'wb') as f:
                        f.write(self.log)
                    result = {'状态': '下载结束','路径':'/LOG/ibox.tar.gz'}
                    self.set_db_data(result, 28, 'avnpara')


                else:
                    self.log += msg

                    # self.logger.info('log is %s, size is %s' % (decode(self.log), len(self.log)))

                if sendMsg:
                    self.logger.info('发送数据%s,CMD:%s' % (hexlify(sendMsg), cmd))

                    self.session.write(sendMsg)
            except Exception as e:
                self.closeFlag = 0
                self.logger.info('log is :%s'%e)

    def gzip_compress(self, raw_data):
        buf = StringIO()
        f = gzip.GzipFile(mode='wb', fileobj=buf)
        try:
            f.write(raw_data)
        finally:
            f.close()
        return buf.getvalue()



    """
    if __name__ == '__main__':
    
    
    
    
    
    
        rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(rootpath)
        os.environ['root_path'] = rootpath
    
        simu = USBIAgree5G.get_instances('192.168.1.1', 8888)
    
        simu.loginApi()
    
        while 1:
            pass

    """


    # 检查FOTA升级包下载状态成功或失败-liuyuanhao
    def QueryRemoteDownloadStatusUpdate1(self, msg, id):
        Status = Common.CommonVar.RemoteDownloadStatusUpdate['Status'].get(int(msg[14:16], 16))
        ECUID = Common.CommonVar.RemoteDownloadStatusUpdate['ECUID'].get(int(msg[16:18], 16))
        NumOfEcus = int(msg[18:20], 16)
        FailReason = Common.CommonVar.RemoteDownloadStatusUpdate['FailReason'].get(int(msg[20:22], 16))
        result = {'Status': Status, 'ECUID': ECUID, 'NumOfEcus': NumOfEcus, 'FailReason': FailReason}
        return result


    # 检查升级完成0311状态，升级中，升级完成-liuyuanhao
    def QueryRemoteReflashStatusUpdate1(self):
        session = Common.CommonVar.Session
        avn_gps = session.query(avn).filter_by(id=17).first()
        result = avn_gps.content
        session.close()
        return result


    # 检查下载进程030F状态-liuyuanhao
    def QueryRemoteReflashCheckUpdate1(self):
        session = Common.CommonVar.Session()
        avn_gps = session.query(avn).filter_by(id=15).first()
        result = avn_gps.content
        session.close()
        return result

    # 检查下载进程0310状态-liuyuanhao
    def QueryRemotedownloadCheckUpdate(self):
        session = Common.CommonVar.Session()
        avn_gps = session.query(avn).filter_by(id=16).first()
        result = avn_gps.content
        session.close()
        return result

    # 检查0312状态-刘源浩
    def QueryRemoteReflashTips1(self):
        session = Common.CommonVar.Session
        avn_gps = session.query(avn).filter_by(id=18).first()
        return avn_gps

    @staticmethod
    def get_instances(host, port):
        if (host, port) not in USBIAgree5G.instancesobj:
            USBIAgree5G.instancesobj[(host, port)] = USBIAgree5G(host, port)
        return USBIAgree5G.instancesobj[(host, port)]
