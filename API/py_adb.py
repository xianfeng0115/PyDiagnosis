# coding:utf-8

import subprocess


class PyAdb:
    """
    adb shell类
    """
    #
    # def __init__(self):
    #     # self.device = device
    #     pass

    def sendCmd(self, cmd):
        self.adb = subprocess.Popen("adb shell %s"%cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        return self.adb.communicate()[0]

# if __name__ == '__main__':
#     adb = PyAdb()
#     print(adb.sendCmd('ping -c 1 www.baidu.com'))
#     pass
