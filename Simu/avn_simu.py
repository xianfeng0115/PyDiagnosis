# coding:utf-8

import json
from tornado.web import RequestHandler
from Common.CommonVar import Session, logger,AvnData,strip,port,USBI_CMD_DICT
from DB.avn_table import AvnSimu as avn
from API.USBI import USBIAgree

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from tornado import gen
import tornado
from Common.CommonFun import *
import Common.CommonVar
from binascii import hexlify, unhexlify

from contextlib import closing
import datetime


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

class BaseHandler(RequestHandler):
    # executor为RequestHandler中的一个属性，在使用run_on_executor时，必须要用，不然会报错
    # executor在此设计中为设计模式中的享元模式，所有的对象共享executor的值
    executor = Executor()
    def initialize(self):
        # self.request.method = 'POST'
        # print(self.request.method, type(self.request.method))
        self.logger = Common.CommonVar.logger
        self.set_default_header()

    def set_default_header(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        # self.set_header('Access-Control-Allow-Origin', 'http://localhost:8080')
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type')


class GetAvnData(BaseHandler):

    @gen.coroutine
    def post(self):
        result =  self.response_msg()
        return_data = json.dumps(result, ensure_ascii=False)

        self.write(return_data)

    def response_msg(self):
        session = Session()
        avn_data = session.query(avn).all()
        avn_new_data = self.db_2_vue(avn_data)
        result = {'avn_data': avn_new_data, 'child_data':{}}
        return result

    def db_2_vue(self, avn_data):
        result = []

        for pid, vue_line in enumerate(avn_data, start=1):
            line = eval(str(vue_line))
            try:
                count_str = eval(line.get('content').replace('null','""')) if line.get('content') != '' else ''
                if len(count_str) >2:
                    result.append(self.add_dict_child(line, pid))
                elif pid ==2:
                    result.append(self.add_dict_child(line, pid))
                else:
                    result.append(line)
            except:
                pass
        return result

    def add_dict_child(self, line,pid):
        result = line
        content_dict = eval(line.get('content').replace('null','""'))
        result['children'] = []
        for sonid,son in enumerate(content_dict, start=1):
            # childDict = {}
            # childDict['id'] = str(pid) + '.' + str(sonid)
            # childDict['type'] = son
            # childDict['content'] = str(content_dict.get(son))
            # childDict['count'] = ''
            # childDict['current'] = ''
            childDictid,childDict = self.set_table(son,str(content_dict.get(son)), pid, sonid)
            if type(content_dict.get(son)) is list:
                childDict['children'] = self.add_list_child(content_dict.get(son), childDictid)
            if type(content_dict.get(son)) is dict:
                childDict['children'] = self.add_list_child(content_dict.get(son).values(), childDictid,title='基站')
            result['children'].append(childDict)
        return result


    def add_list_child(self, childlist,pid,title='卫星'):
        result = []
        for childid, child in enumerate(childlist, start=1):
            child_result_id, child_result = self.set_table('%s%d'%(title, childid), '详细...', pid, childid)
            son_list = []
            for sonid, son in enumerate(child, start=1):
                id,son_result = self.set_table(son,child.get(son),child_result_id, sonid)
                son_list.append(son_result)
                child_result['children'] =son_list
            result.append(child_result)
        return result


    def set_table(self, key,value, pid, sonid):
        childDict = {}
        childDict['id'] = str(pid) + '.' + str(sonid)
        childDict['type'] = key
        childDict['content'] = value
        childDict['count'] = ''
        childDict['current'] = ''
        return childDict['id'],childDict

    def db_2_dict(self, avn_data):
        result = []
        for pid,r in enumerate(avn_data,start=1):
            #result[avn_data.index(r)] = eval(str(r))
            para_dict = eval(str(r))
            child = []

            try:
                content_dict = eval(para_dict.get('content')) if para_dict.get('content')!='' else {}
            except:
                pass
            for id,content_key in enumerate(content_dict, start=1):
                childDict = {}
                iter_index = 10
                childDict['id'] = str(pid) + '.' +str(id)
                childDict['type'] = content_key
                childDict['count'] = r.count
                childDict['current'] = r.current.strftime('%Y-%m-%d %H:%M:%S')
                if type(content_dict.get(content_key)) is dict:

                    children = self.set_child(content_dict.get(content_key), childDict['id'], iter_index*10)
                    if children:
                        para_dict['children'] = children
                elif type(content_dict.get(content_key)) is list:
                    children = self.set_childlist(content_dict.get(content_key), childDict['id'])
                    if children:
                        para_dict['children'] = children

                childDict['content'] = content_dict.get(content_key)
            if 'creatime' in para_dict:
                del para_dict['creatime']
                del para_dict['_locked']
            result.append(para_dict)
        return result

    def set_childlist(self,child,pid):
        child_list = []
        if child:
            for id, son in enumerate(child, start=1):
                pass

    def set_child(self, child,pid,iter_index):
        child_list = []
        if child:
            for id,son in enumerate(child, start=1):
                if type(child.get(son)) is not dict:
                    childDict = {}
                    childDict['id'] = str(pid) + '.' + str(id)
                    childDict['type'] = son
                    childDict['content'] = child.get(son)
                    childDict['count'] = ''
                    childDict['current'] = ''
                    child_list.append(childDict)
                else:
                    childDict = {}
                    childDict['id'] = pid + '.' + str(id)
                    childDict['type'] = '详细信息'
                    childDict['content'] = '...'
                    childDict['count'] = ''
                    childDict['current'] = ''
                    child_son = self.set_child(child.get(son),childDict['id'], iter_index*10)
                    childDict['children'] = child_son

                    child_list.append(childDict)

        return child_list




class IboxLogin(BaseHandler):

    def post(self):
        try:
            host = self.get_argument('serverip')
            port = self.get_argument('serverport')
            USBI = USBIAgree.get_instances(host, port)
            USBI.connect_socket()
            session = USBI.session

            #with closing(session):
            if session:
                USBI.sendMsg('0001')

                result = {'result': 0, 'Conn': 1}
                return_data = json.dumps(result, ensure_ascii=False)
                self.write(return_data)

        except Exception as e:
            result = {'result': 1, 'Conn': 1, 'error': e}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

    def put(self):
        try:
            result = {'result': 0, 'Conn': 0}
            host = self.get_argument('serverip')
            port = self.get_argument('serverport')
            return_data = json.dumps(result, ensure_ascii=False)
            usbi = USBIAgree.get_instances(host, port)
            if usbi.session:
                usbi.handle_close()
            self.write(return_data)
        except Exception as e:
            result = {'result': -1, 'Conn': 1, 'error': e}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)


    def options(self):
        result = {'result': 0}
        return_data = json.dumps(result, ensure_ascii=False)
        self.write(return_data)


class CheckAVN(BaseHandler):

    def post(self):
        try:
            return_data = self.response_msg()
            self.write(return_data)
        except Exception as e:
            result = {'result': -1, 'Conn': 1, 'error': e}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

    def response_msg(self):
        strip = self.get_argument('serverip')
        port = self.get_argument('serverport')
        index = self.get_argument('index')
        cmd = USBI_CMD_DICT.get(index)
        if strip and port:
            USBI = USBIAgree.get_instances(strip, port)
            session = USBI.session
            if session:
                result_return = USBI.sendMsg(cmd)
                result = {'result': 0, 'Conn': 1, 'result_return': str(result_return)}
                return_data = json.dumps(result, ensure_ascii=False)
                return return_data
            else:
                result = {'result': -1, 'Conn': 1, 'error': 'connect tcp error'}
                return_data = json.dumps(result, ensure_ascii=False)
                return return_data
    def put(self):
        try:
            strip = self.get_argument('serverip')
            port = self.get_argument('serverport')
            index = self.get_argument('index')
            cmd = index.lower()
            if strip and port:
                USBI = USBIAgree.get_instances(strip, port)
                session = USBI.session
                if session:
                    USBI.sendMsg(cmd)
                    result = {'result': 0, 'Conn': 1}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)
                else:
                    result = {'result': -1, 'Conn': 1, 'error': 'connect tcp error'}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)

        except Exception as e:
            result = {'result': -1, 'Conn': 1, 'error': e}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

    def options(self):
        result = {'result': 0}
        return_data = json.dumps(result, ensure_ascii=False)
        self.write(return_data)


class telematics_Call(BaseHandler):

    def post(self):
        try:
            strip = self.get_argument('serverip')
            port = self.get_argument('serverport')
            CallType = self.get_argument('CallType')
            CallCenterID = self.get_argument('CallCenterID')
            cmd = '0203'
            if strip and port:
                USBI = USBIAgree.get_instances(strip, port)
                session = USBI.session
                if session:
                    USBI.sendMsg(cmd, CallType=CallType, CallCenterID=CallCenterID)
                    result = {'result': 0, 'Conn': 1}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)
                else:
                    result = {'result': -1, 'Conn': 1, 'error': 'connect tcp error'}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)

        except Exception as e:
            result = {'result': -1, 'Conn': 1, 'error': e}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

class RemoteReflash_Check(BaseHandler):

    def post(self):
        try:
            strip = self.get_argument('serverip')
            port = self.get_argument('serverport')
            DataValue = self.get_argument('DataValue')
            cmd = '0207'
            if strip and port:
                USBI = USBIAgree.get_instances(strip, port)
                session = USBI.session
                if session:
                    USBI.sendMsg(cmd, DataValue=DataValue)
                    result = {'result': 0, 'Conn': 1}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)
                else:
                    result = {'result': -1, 'Conn': 1, 'error': 'connect tcp error'}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)

        except Exception as e:
            result = {'result': -1, 'Conn': 1, 'error': e}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

class RemoteReflash_Perform(BaseHandler):

    def post(self):
        try:
            strip = self.get_argument('serverip')
            port = self.get_argument('serverport')
            ex_ECU_ID = self.get_argument('ex_ECU_ID')
            ReflashReqInfo = self.get_argument('ReflashReqInfo')
            cmd = '0208'
            if strip and port:
                USBI = USBIAgree.get_instances(strip, port)
                session = USBI.session
                if session:
                    USBI.sendMsg(cmd, ex_ECU_ID=ex_ECU_ID, ReflashReqInfo=ReflashReqInfo)
                    result = {'result': 0, 'Conn': 1}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)
                else:
                    result = {'result': -1, 'Conn': 1, 'error': 'connect tcp error'}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)

        except Exception as e:
            result = {'result': -1, 'Conn': 1, 'error': e}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

class Booking_UpdateTime(BaseHandler):

    def post(self):
        try:
            strip = self.get_argument('serverip')
            port = self.get_argument('serverport')
            ECU_ID = self.get_argument('ECU_ID')
            DATE = self.get_argument('DATE')
            cmd = '020d'
            if strip and port:
                USBI = USBIAgree.get_instances(strip, port)
                session = USBI.session
                if session:
                    USBI.sendMsg(cmd, ECU_ID=ECU_ID, DATE=DATE)
                    result = {'result': 0, 'Conn': 1}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)
                else:
                    result = {'result': -1, 'Conn': 1, 'error': 'connect tcp error'}
                    return_data = json.dumps(result, ensure_ascii=False)
                    self.write(return_data)

        except Exception as e:
            result = {'result': -1, 'Conn': 1, 'error': e}
            return_data = json.dumps(result, ensure_ascii=False)
            self.write(return_data)

class resetbox(BaseHandler):

    def post(self):
        strip = self.get_argument('serverip')
        port = self.get_argument('serverport')
        reset_value = self.get_argument('reset_value')
        if strip and port:
            USBI = USBIAgree.get_instances(strip, port)
            session = USBI.session
            if session:
                USBI.sendMsg('0209',reset_value=reset_value)
                result = {'result': 0}
                return_data = json.dumps(result, ensure_ascii=False)
                self.write(return_data)

class setFault(BaseHandler):

    def post(self):
        strip = self.get_argument('serverip')
        port = self.get_argument('serverport')
        if strip and port:
            USBI = USBIAgree.get_instances(strip, port)
            session = USBI.session
            if session:
                USBI.nosendlist.append('0301')
                USBI.nosendlist.append('0304')
                result = {'result': 0}
                return_data = json.dumps(result, ensure_ascii=False)
                self.write(return_data)



