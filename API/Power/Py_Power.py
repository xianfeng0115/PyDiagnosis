import pyvisa as visa


class Power():

    def __init__(self):
        rm = visa.ResourceManager()
        res = rm.list_resources()
        for name in res:
            if 'ASRL' in name:
                try:
                    self.Power_inst = rm.open_resource(name)
                except:
                    pass
            # elif 'TCP' in name:
            #     self.Meas_inst = rm.open_resource(name)
        welcome = self.Power_inst.query("*IDN?")
        self.Power_inst.write("SYSTEM:REMOTE")

        print(welcome)

    def Power_on(self):
        self.Power_inst.write("OUTP ON")

    def Power_off(self):
        self.Power_inst.write("OUTP OFF")

    def set_power_VOLT(self, VoLT):
        self.Power_inst.write("VOLT %s"%VoLT)

    def set_power_CURR(self, VoLT):
        self.Power_inst.write("CURR %s"%VoLT)

    def get_power_CURR(self):
        return self.Power_inst.query("MEAS:CURR?")

    def get_power_VOLT(self):
        return self.Power_inst.query("MEAS:VOLT?")

    # def Meas_off(self):
    #     self.Meas_inst.write("OUTP OFF")
    #
    # def Meas_on(self):
    #     self.Meas_inst.write("OUTP ON")

if __name__ == "__main__":
    p = Power()
    p.Power_off()
    p.Power_on()
#     p.set_power_VOLT(0.6)
#     p.set_power_CURR(0.008)
#     import time
#     time.sleep(1)
#
#     # p.set_power_VOLT(12)
#     print(p.get_power_CURR())
#     print(p.get_power_VOLT())
#     # p.Power_off()
#
#     pass