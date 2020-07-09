# coding:utf-8

import os
import logging
import uuid
from logging import Handler, FileHandler, StreamHandler


class PathFileHandler(FileHandler):
    def __init__(self, path, filename, mode='a', encoding=None, delay=True):

        filename = os.fspath(filename)
        if not os.path.exists(path):
            os.mkdir(path)
        self.baseFilename = os.path.join(path, filename)
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        # if delay:
        Handler.__init__(self)
        self.stream = None
        # else:
        #     StreamHandler.__init__(self, self._open())


class Loggers(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING,
        'error': logging.ERROR, 'critical': logging.CRITICAL
    }
    instancesobj = {}

    def __init__(self, filename='{uid}.log'.format(uid=uuid.uuid4()), level='info', log_dir='log', logtype='console',
                 logmode='w', fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        abspath = os.path.dirname(os.path.abspath(__file__))
        self.directory = os.path.join(abspath, log_dir)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        file_handler = PathFileHandler(path=self.directory, filename=filename, mode=logmode, encoding='utf-8')
        file_handler.setFormatter(format_str)
        if logtype == 'all':
            stream_handler = logging.StreamHandler()
            self.logger.addHandler(stream_handler)
            self.logger.addHandler(file_handler)
        elif logtype == 'console':
            stream_handler = logging.StreamHandler()
            self.logger.addHandler(stream_handler)
        else:
            self.logger.addHandler(file_handler)

    @staticmethod
    def get_instances(**keywords):
        name = keywords.get('filename')
        if name not in Loggers.instancesobj:
            Loggers.instancesobj[name] = Loggers(**keywords).logger
        return Loggers.instancesobj[name]


if __name__ == "__main__":
    txt = '日志测试'
    log = Loggers.get_instances(filename='测试.log', log_dir='../Log', logtype='all')
    log.info(4)
    log.info(5)
    log.info(txt)