#coding:utf-8
import json
from API.py_ssh import *
import asyncore
import queue
import re
import threading
from binascii import hexlify
from API.Logger import *

class Client(asyncore.dispatcher):

    def __init__(self):
        asyncore.dispatcher.__init__(self)

        self.logger = Loggers.get_instances(filename='TestCase.log')
        self.create_socket()
        self.rev_que = queue.Queue()
        self.send_que = queue.Queue()
        self.id = 0
        self.rev_msg =b''
        self.buf = b''
        self.lock_id = threading.Lock()



    def handle_read(self):
        try:
            data = self.recv(65536)
            self.logger.info('handle_read msg：%s' %data)
            if data:
                if b'}{"' in data:
                    msg_list = self.split_json(data)
                    for sigle_msg in msg_list:
                        self.sigled_msg_handle(sigle_msg, bufFlag=str(msg_list.index(sigle_msg)))
                else:
                    self.sigled_msg_handle(data)

        except Exception as e:
            self.logger.info('handle_read error:%s,%s'%(data,self.rev_msg))

    def split_json(self, morejson):
        rev_list = morejson.split(b'}{')
        result = []
        for index in range(len(rev_list)):
            if index == 0:
                result.append(rev_list[index] + b'}')
            elif index == len(rev_list) - 1:
                result.append(b'{' + rev_list[index])
            else:
                result.append(b'{' + rev_list[index] + b'}')
        return result

    def sigled_msg_handle(self, data, bufFlag=None):

        if self.is_json(data):
            self.rev_msg = data
        else:
            if bufFlag:
                if bufFlag == '0':
                    self.buf += data[1:]
                else:
                    self.buf += data[:-1]
            else:
                self.buf += data
            if self.is_json(self.buf):
                self.rev_msg = self.buf
                self.buf = b''
        if self.rev_msg:
            rev_msg = json.loads(self.decode(self.rev_msg))
            self.rev_msg = b''
            self.logger.info("#############client recv   #################\n%s" %rev_msg)
            self.logger.info("#############client recv end#################")
            self.rev_que.put(rev_msg)


    def is_json(self, myjson):
        try:
            json_object = json.loads(self.decode(myjson))
        except Exception as e:
            logging.info('json error:%s' % e)
            try:
                if '{' not in self.decode(myjson):
                    return False
                else:
                    json_object = eval(self.decode(myjson))
            except Exception as e:
                logging.info('json error:%s' % e)
                return False
        return True
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

    def sendMsg(self, method, result=0,params={},threadCount=1,processCount=1,libname=''):
        try:
            self.lock_id.acquire()
            id = self.id + 1
            if id == 33:
                pass
            self.id += 1
            #hex_params = self.set_para(params)
            params_to_list = [(line,params.get(line)) for line in params]
            m = {"type": "req", "method": method, "result": result, "param": params_to_list, "id": id,
                 "threadCount":threadCount,"processCount":processCount}
            send_msg = json.dumps(self.encode(m), ensure_ascii=False)
            self.send_que.put(send_msg)

            while 1:
                boolflag = not self.rev_que.empty()
                if boolflag:
                    msg = self.rev_que.get()
                    if id == msg.get('id'):
                        break

                    else:
                        self.rev_que.put(msg)
            self.lock_id.release()


            return msg
        except Exception as e:
            self.logger.info('sendMsg error is %s'%e)


    def sendwaiteMsg(self, method, result=0,params={},threadCount=1,processCount=1,waite=12):
        try:
            self.lock_id.acquire()
            id = self.id + 1
            if id == 33:
                pass
            self.id += 1
            params_to_list = [(line,params.get(line)) for line in params]
            m = {"type": "req", "method": method, "result": result, "param": params_to_list, "id": id,
                 "threadCount":threadCount,"processCount":processCount}
            send_msg = json.dumps(self.encode(m), ensure_ascii=False)
            self.send_que.put(send_msg)
            now = 0
            msg_list = []
            while now <= waite:
                now += 1
                boolflag = not self.rev_que.empty()
                if boolflag:
                    msg_list.append(self.rev_que.get())
                else:
                    time.sleep(1)

            self.lock_id.release()


            return msg_list
        except Exception as e:
            self.logger.info('sendMsg error is %s'%e)

    def set_para(self, para):
        result = {}
        for key in para:
            if len(para.get(key))>2:
                result[key] = self.decode(hexlify(self.encode(para.get(key)[0])))
            else:
                result[key] = para.get(key)
        return result


    def handle_write(self):
        try:
            if not self.send_que.empty():
                sendmsg = self.send_que.get()
                self.logger.info("#############client request    #################\n%s"%sendmsg)
                self.logger.info("#############client request end#################")
                self.send(self.encode(sendmsg))

                # buffer = 1024
                # i = 0
                # data_len = len(sendmsg)
                # while data_len > 0:
                #     if data_len >= buffer:
                #         content = sendmsg[i * buffer:(i + 1) * buffer]
                #         self.send(content)
                #         data_len -= buffer
                #         i += 1
                #     else:
                #         content = sendmsg[i * buffer:]
                #         self.send(content)
                #         data_len = 0
        except Exception as e:
            self.logger.info('handle_write error is %s'%e)



class EchoClientThread(threading.Thread):
    def __init__(self,strip, port, user_name, password):
        threading.Thread.__init__(self)
        self.strip =strip
        self.port = port
        self.user_name = user_name
        self.password = password
        self.client = Client()

    def run(self):

        self.client.connect((self.strip, self.port))
        asyncore.loop()

    def is_alive(self):
        conn = 0
        try:
            self.client.connect((self.strip, self.port))
            if self.client and self.client.connected == True:
                conn = 1
        except Exception as e:
            conn = 0
        finally:
            return conn


    def pushServerAndStart(self):

        diassshmgr = DIASSshManager(self.strip, self.user_name, self.password)
        # 当前文件的路径
        pwd = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'Ibox')
        server_env = os.path.join(pwd, "python3_dsp_install.tar.gz")
        server_path = os.path.join(pwd, "session.py")
        diassshmgr.exec_command("killall -9  *python3*")
        # diassshmgr.exec_command("rm -r /saic/AutoTest/")
        diassshmgr.exec_command('mkdir /saic/AutoTest/')
        diassshmgr.put(server_env, "/saic/AutoTest/python3_dsp_install.tar.gz")
        diassshmgr.put(server_path, "/saic/AutoTest/session.py")
        out = diassshmgr.exec_command("chmod 777 /saic/AutoTest/python3_dsp_install.tar.gz")
        out = diassshmgr.exec_command("cd /saic/AutoTest/;tar -xf /saic/AutoTest/python3_dsp_install.tar.gz")
        #out = diassshmgr.exec_command("ln -s /saic/AutoTest/python3/bin/python3  /usr/bin/python37")
        out = diassshmgr.exec_command("chmod 777 /saic/AutoTest/session.py")
        out = diassshmgr.ssh.exec_command("cd /saic/AutoTest/python3/bin/;./python3.7 /saic/AutoTest/session.py &  >/tmp/AutoTest/app.log &")
        #out = diassshmgr.ssh.exec_command("nohup python37 /saic/AutoTest/session.py  > /saic/AutoTest/lu.log 2>&1  &")
        time.sleep(1)

    def push5GServerAndStart(self, libname='hsm'):

        diassshmgr = DIASSshManager(self.strip, self.user_name, self.password)
        # 当前文件的路径
        pwd = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'Ibox')
        server_env = os.path.join(pwd, "m2000.ini")
        server_path = os.path.join(pwd, "session5g.py")
        # diassshmgr.exec_command("killall -9  python3")
        diassshmgr.exec_command('mkdir /tmp/AutoTest/')
        diassshmgr.put(server_env, "/tmp/AutoTest/m2000.ini")
        diassshmgr.put(server_path, "/tmp/AutoTest/session5g.py")
        # out = diassshmgr.exec_command("chmod 777 /tmp/AutoTest/python3_dsp_install.tar.gz")
        # out = diassshmgr.exec_command("cd /tmp/AutoTest/;tar -xf /tmp/AutoTest/python3_dsp_install.tar.gz")
        out = diassshmgr.exec_command("chmod 777 /tmp/AutoTest/session5g.py")
        out = diassshmgr.ssh.exec_command('export LD_LIBRARY_PATH="/lib/";export LD_LIBRARY_PATH="/usr/lib/";\
                                          export LD_LIBRARY_PATH="/diasapp/lib/"; mount -o remount -rw /;ldconfig;\
                                          cd /tmp/AutoTest/;python3 session5g.py %s &  > /tmp/AutoTest/app.log &'%libname)
        time.sleep(1)


    def stopServerAnddelete(self):
        diassshmgr = DIASSshManager(self.strip, self.user_name, self.password)
        # 当前文件的路径
        pwd = os.path.dirname(__file__)
        diassshmgr.exec_command("killall - 9 python37")
        diassshmgr.exec_command("rm -r /saic/AutoTest/")
        diassshmgr.exec_command("rm -r /usr/bin/python37")
        time.sleep(0.2)
