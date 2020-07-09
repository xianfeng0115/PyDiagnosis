#coding:utf-8
import visa


class Meas():

    def __init__(self):
        rm = visa.ResourceManager()
        res = rm.list_resources()
        for name in res:
            if 'TCP' in name:
                 self.Meas_inst = rm.open_resource(name)
        welcome = self.Meas_inst.query("*IDN?")
        self.Meas_inst.write("SYSTEM: REMOTE")

        print(welcome)

    def Meas_on(self):
        self.Meas_inst.write("OUTP ON")

    def Meas_off(self):
        self.Meas_inst.write("OUTP OFF")

    def set_Meas_VOLT(self, VoLT):
        self.Meas_inst.write("VOLT %s" % VoLT)

    def set_Meas_CURR(self, VoLT):
        self.Meas_inst.write("CURR %s" % VoLT)

    def get_Meas_CURR(self):
        return self.Meas_inst.query("MEAS:CURR?")

    def get_Meas_VOLT(self):
        return self.Meas_inst.query("MEAS:VOLT?")

    # def Meas_off(self):
    #     self.Meas_inst.write("OUTP OFF")
    #
    # def Meas_on(self):
    #     self.Meas_inst.write("OUTP ON")


if __name__ == "__main__":
    p = Meas()

    p.Meas_on()
    p.set_Meas_VOLT(12)
    print(p.get_Meas_CURR())
    print(p.get_Meas_VOLT())
    p.Meas_off()
    pass