import paramiko
from API.scp import SCPClient
from contextlib import suppress
from contextlib import closing
import time
import queue
import threading
from API.pyat import *
from threading import Thread

class DIASSshManager:
    def __init__(self, ip, username, password = None):
        ssh = paramiko.SSHClient()
        self.ssh = ssh
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.queue_data = queue.Queue()
        self.save_flag = 0
        self.send_mornitor()
        self.com_send = ATHandle('COM4')
        if password is None:
            with suppress(paramiko.ssh_exception.SSHException):
                ssh.connect(ip, username = username, password=password)
            ssh.get_transport().auth_none(username)
        else:
            ssh.connect(ip, username = username, password=password)

        self.ssh = ssh

    def put(self, files, remote_path=b'.', preserve_times=False):
        with closing(SCPClient(self.ssh.get_transport())) as scp:
            scp.put(files, remote_path = remote_path, preserve_times = preserve_times)

    def get(self, remote_path, local_path='', preserve_times=False):
        with closing(SCPClient(self.ssh.get_transport())) as scp:
            scp.get(remote_path, local_path=local_path, preserve_times=False)

    def exec_command(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return ''.join(stdout.readlines())

    def exec_step_command(self,cmdlist):
        chan = self.ssh.invoke_shell()
        for cmd in cmdlist:
            chan.send(cmd+'\n')
            time.sleep(0.1)
            res = chan.recv(1024)
            if b'Gnss RTCMData' in res:
                self.save_flag =1
            if self.save_flag:
                self.queue_data.put(res)
                while 1:
                    res = chan.recv(1024)
                    if res:
                        self.queue_data.put(res)
        return res

    def send_mornitor(self):
        t1 = threading.Thread(target=self.send_func)
        t1.setDaemon(True)
        t1.start()

    def send_func(self):
        while 1:
            if not self.queue_data.empty():
                data = self.queue_data.get()
                self.com_send.send_data(data)
    def start_damon(self, path):
        stdin, stdout, stderr = self.ssh.exec_command(path)


if __name__ =="__main__":
    z = DIASSshManager("192.168.1.18", "root","Dgyus@312893")
    #Dgyus@312893
    z.exec_step_command(['cd /diasapp/app', 'export LD_LIBRARY_PATH="/diasapp/lib"','./diasdebugoutput', 'rtcmon'])
    # z.put("G:\\v2x\\bserver\\s", "/tmp/s")
    # o = z.exec_command("chmod 755 /tmp/s")
    # print(o)
    # z.start_damon("/tmp/s")

    time.sleep(50)
