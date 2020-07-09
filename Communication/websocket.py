import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options
import time
import logging
import uuid
import sys,os
import json
from tornado.options import define, options


define('port', default=8090, help="The tornado server port", type=int)


class WebSocketSever(tornado.websocket.WebSocketHandler):
    bao_cons = set()
    bao_waiters = {}
    con_key = None
    webname = ''

    def open(self):
        sole_id = str(uuid.uuid4()).upper()
        self.con_key = sole_id
        self.bao_waiters[self.webname] = self
        self.write_message({"websocket_sole_id": sole_id})
        logging.info("websocket opened!")

    @classmethod
    def send_message(self, message, webname):

        if message == "close":
            self.close()
            return
        try:
            parse_data = tornado.escape.json_decode(message)
            self.bao_waiters[webname].write_message(parse_data)
        except:
            try:
                self.bao_waiters[webname].write_message(message)
            except:
                send_msg = json.dumps(message, ensure_ascii=False)
                self.bao_waiters[webname].write_message(send_msg)

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


    def check_origin(self, str):
        return True

    def allow_draft76(self):
        return True
    @classmethod
    def on_close(self):
        if self.webname:
            self.bao_waiters.pop(self.webname)

        logging.info("websocket closed!")

class BcmWebSocket(WebSocketSever):


    webname = 'bcm'


class Application(tornado.web.Application):
    def __init__(self, handlers, setting):
        super(Application, self).__init__(handlers, **setting)


def main():
    options.parse_command_line()
    handlers = [(r"/websocket", WebSocketSever)]
    setting = dict(xsrf_cookies=False)
    app = Application(handlers, setting)
    print(options.port)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
