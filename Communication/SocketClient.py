# coding:utf-8

from tornado import ioloop, gen, iostream
from binascii import hexlify,unhexlify
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from Common.CommonFun import *
import socket
import queue



class Executor(ThreadPoolExecutor):
    """ 创建多线程的线程池，线程池的大小为10
    创建多线程时使用了单例模式，如果Executor的_instance实例已经被创建，
    则不再创建，单例模式的好处在此不做讲解
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=200)
        return cls._instance


class BaseClient:

    instancesobj = {}
    executor = Executor()
    def __init__(self, host, port):
        self.closeFlag = 1
        self.host = host
        self.port = port
        self.msg_que = queue.Queue()
        self.session = None
        # import tornado
        # self.loop = tornado.ioloop.IOLoop.instance()

        pass

    # @run_on_executor
    # def connect_api(self):
    #
    #     self.connect_socket()
    #
    # def start_api(self):
    #     self.loop.run_sync(self.connect_socket)
    #     pass

    @gen.coroutine
    def connect_socket(self):
        try:
            self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            self.session = iostream.IOStream(self.sock_fd)

            yield self.session.connect((self.host, int(self.port)))


            # self.session = TCPClient()
            # self.session.connect(self.host, self.port, self.morniting)

            yield self.morniting()






        except Exception as e:
            raise


    def on_close(self):
        pass

    @gen.coroutine
    def morniting(self):
        while self.closeFlag:
            yield self.handle_read()
            yield self.handle_msg()

    @gen.coroutine
    def handle_msg(self):
            if not self.msg_que.empty():
                msg = self.msg_que.get()

                #self.long_handle(msg)
                cmdlist = self.parse_cmd(msg)
                for cmd in cmdlist:
                    sendMsg = self.handle_sendmsg(cmd,  decode(hexlify(msg)))

                    if sendMsg:
                        cmd = hexlify(sendMsg)[8:10] + hexlify(sendMsg)[6:8]
                        self.logger.info('发送数据%s,CMD:%s' % (hexlify(sendMsg),cmd))

                        yield self.session.write(sendMsg)

    @run_on_executor
    def long_handle(self, msg):
        cmdlist = self.parse_cmd(msg)
        for cmd in cmdlist:
            sendMsg = self.handle_sendmsg(cmd, decode(hexlify(msg)))

            if sendMsg:
                cmd = hexlify(sendMsg)[8:10] + hexlify(sendMsg)[6:8]
                self.logger.info('发送数据%s,CMD:%s' % (hexlify(sendMsg), cmd))
                self.session.write(sendMsg)


    def sendMsg(self, cmd, msg=None, **kwargs):
        sendMsg = self.handle_sendmsg(cmd, msg=msg, **kwargs)
        if sendMsg:
            self.logger.info('发送数据%s,CMD:%s' % (hexlify(sendMsg), cmd))
            try:
                self.session.write(sendMsg)
            except Exception as e:
                self.logger.error('发送数据错误：%s'%e)


    def handle_sendmsg(self, cmd, msg, **kwargs):
        pass

    def handle_close(self):
        self.closeFlag = 0
        self.session.close()
        if (self.host, self.port) in self.instancesobj:
            del self.instancesobj[(self.host, self.port)]

    @gen.coroutine
    def handle_read(self):
        try:
                msg = yield self.session.read_bytes(32768, partial=True)
                cmd = hexlify(msg)[8:10] + hexlify(msg)[6:8]
                self.logger.info('接受数据%s,CMD:%s' % (hexlify(msg),cmd))
                self.msg_que.put_nowait(msg)
                #yield self.handle_msg(msg)
                #self.handle_msg(msg)
                # rev_msg = hexlify(back)
                # cmdWord = rev_msg[8:10] + rev_msg[6:8]
        except Exception as e:
            # raise
            # self.logger.info(e)
            self.handle_close()
            yield




    @staticmethod
    def get_instances(host, port):
        if (host, port) not in BaseClient.instancesobj:
            BaseClient.instancesobj[(host, port)] = BaseClient(host, port)
        return BaseClient.instancesobj[(host, port)]

