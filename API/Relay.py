# coding:utf-8
import os
from ctypes import *
from API.Py_excle import *
apipath = os.path.dirname(os.path.abspath(__file__))
LIBCRYPTO_PATH = os.path.join(apipath, 'python_lib.dll')

class RelayHandle:
    """
       控制继电器
    """

    def __init__(self):
        lib = CDLL(LIBCRYPTO_PATH, mode=RTLD_GLOBAL)
        self.relay_inst_method = lib.ControlDigit
        self.relay_inst_method.argtypes = [c_wchar_p, c_int, c_int]
        self.relay_inst_method.restype = c_int
        self.power, self.ground, self.signal = pyExcel.get_instances().relay_cfg
        self.relay_state = {'power':0,'ground':0,'signal':0}
        pass

    def set_digit_name(self, digit_name, port):
        self.divce_name = c_wchar_p(digit_name)
        self.port = c_int(port)

    def send_digit_signal(self, cmd):
        data = c_int(cmd)
        result = self.relay_inst_method(self.divce_name, self.port, data)
        return result

    """
       控制继电器PCIE-1762H,BID#15,实现对电源短接
       参数说明：
       1. cmd表示要对哪个继电器进行操作，例如如果对R5_COM和R5_OUT组成的继电器进行操作，应当cmd=32
       2. relay_port在配置文档中的继电器端口一列，取值范围0-1,表示不同的继电器端口
       3. myaction为本次的动作，取值范围[0,1]，其中0表示断开继电器，1表示链接继电器
    """
    def send_power_signal(self, cmd, relay_port=0, myaction=0):
        self.relay_state['power'] = self.comparestate(self.relay_state['power'], cmd, myaction)
        relay_group = self.power.get('relay_group')
        port = c_int(relay_port)
        divce_name = c_wchar_p(relay_group)
        result = self.relay_inst_method(divce_name, port, self.relay_state['power'])
        return result

    """
       控制继电器PCIE-1762H,BID#14,实现对地短接
       参数说明：
       1. cmd表示要对哪个继电器进行操作，例如如果对R5_COM和R5_OUT组成的继电器进行操作，应当cmd=32
       2. relay_port在配置文档中的继电器端口一列，取值范围0-1,表示不同的继电器端口
       3. myaction为本次的动作，取值范围[0,1]，其中0表示断开继电器，1表示链接继电器
    """
    def send_ground_signal(self,  cmd, relay_port=0, myaction=0):
        self.relay_state['ground'] = self.comparestate(self.relay_state['ground'], cmd, myaction)
        relay_group = self.ground.get('relay_group')
        port = c_int(relay_port)
        divce_name = c_wchar_p(relay_group)
        result = self.relay_inst_method(divce_name, port, self.relay_state['ground'])
        return result

    """
       控制继电器PCIE-1762H,BID#07,实现信号线之间短接
       参数说明：
       1. cmd表示要对哪个继电器进行操作，例如如果对R5_COM和R5_OUT组成的继电器进行操作，应当cmd=32
       2. relay_port在配置文档中的继电器端口一列，取值范围0-1,表示不同的继电器端口
       3. myaction为本次的动作，取值范围[0,1]，其中0表示断开继电器，1表示链接继电器
    """
    def send_signal_signal(self, cmd, relay_port=0, myaction=0):
        self.relay_state['signal'] = self.comparestate(self.relay_state['ground'], cmd, myaction)
        relay_group = self.signal.get('relay_group')
        port = c_int(relay_port)
        divce_name = c_wchar_p(relay_group)
        result = self.relay_inst_method(divce_name, port, self.relay_state['signal'])
        return result

    def comparestate(self, oldstate, cmd, myaction):
        if myaction:
            cmd = oldstate | cmd
        elif 0 != (oldstate & cmd):
            cmd = oldstate ^ cmd
        return cmd

    """
       控制继电器实现div天线是否和地短接
       参数说明：myaction为本次的动作，取值范围（0,1），其中0表示断开继电器，1表示链接继电器
    """
    def set_div_antenna_ground(self, myaction):
        result = self.send_ground_signal(2, 0, myaction)
        return result

    def set_usb_power_off(self, myaction):
        result = self.send_ground_signal(1, 0, myaction)
        return result

    def set_div2_antenna_ground(self):
        pass

    def set_CV2X_antenna_ground(self):
        pass

    def set_GPS_antenna_ground(self):
        pass

    def set_FICM_USB_(self):
        pass

    def set_FICM_antenna_ground(self):
        pass

if __name__ == '__main__':
    relay = RelayHandle()
    # relay.set_digit_name('PCIE-1762H,BID#14', 0)
    # relay.send_signal_signal(255)
    relay.set_digit_name('PCIE-1762H,BID#14', 1)
    relay.send_signal_signal(255)
    relay.set_digit_name('PCIE-1762H,BID#15', 0)
    relay.send_signal_signal(255)
    relay.set_digit_name('PCIE-1762H,BID#15', 1)
    relay.send_signal_signal(255)
    relay.set_digit_name('PCIE-1762H,BID#7', 0)
    relay.send_signal_signal(255)
    relay.set_digit_name('PCIE-1762H,BID#7', 1)
    relay.send_signal_signal(255)
    pass
    # print (relay.send_signal_signal(1))
    # print (relay.set_div_antenna_ground(0))