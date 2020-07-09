#coding:utf-8
import subprocess

class wifi_handle:
    """
        wifi操作指南
    """

    def __init__(self):
       pass

    def connect_wifi(self, name):
        cmd = subprocess.Popen("netsh wlan connect name=%s"%name ,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return_log =  cmd.communicate()[0].decode('gbk')
        if '已成功完成连接请求' in return_log:
            return True
        else:
            return False

    def disconect_wifi(self):

        cmd = subprocess.Popen("netsh wlan disconnect" ,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    def set_wlan(self):

        cmd = subprocess.Popen('Netsh WLAN add profile filename="./WLAN.xml" ',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

if __name__ == '__main__':
    wifi = wifi_handle()
    wifi.set_wlan()
    a = wifi.connect_wifi('小米手机')

    # a = wifi.connect_wifi('DIAS_STAFF')
    wifi.disconect_wifi()
    pass


