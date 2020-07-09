from API.pyCAN_5G import *
import datetime

class Diagnosis():
    def __init__(self):
        self.canMsg = CANAPI_5G()
        self.excel = pyExcel()
        self.ExpectResult = self.excel.can_dict
    def SeedNetworkMessage(self):
        self.network_msg = {'ID': '41F', 'DATA': ['02', '70', '01', '00', '00', '00', '00', '00']}
        self.canMsg.Timing_send_can(self.network_msg,0.010, display=0)

    def ReadInternal(self,CANcmd):
        self.result = self.canMsg.SendMsgFormanyResp(CANcmd,'71c')
        return self.result

    def ResultProcess_bcd(self,DID):
        seedcmd = {'ID': '714', 'DATA': ['03', '22', '%s'%DID[0:2], '%s'%DID[2:], '00', '00', '00', '00']}
        self.ReadResult = self.ReadInternal(seedcmd)
        self.ActualResult = ''
        # 如果回复的报文为单帧，从第四位开始截取，如果为多帧，从第五问开始截取
        if len(self.ReadResult) == 1:
            split_num = 4
        else:
            split_num = 5
        # 计算出BCD码
        for i in self.ReadResult[0]['DATA'][split_num:]:
            self.ActualResult = self.ActualResult + i
        for k in range(1,len(self.ReadResult)):
            for i in self.ReadResult[k]['DATA'][1:]:
                self.ActualResult = self.ActualResult + i
        self.ExpectResult = str(self.ExpectResult['%s'%DID])
        return (self.ActualResult, self.ExpectResult)

    def ResultProcess_ascii(self,DID):
        seedcmd = {'ID': '714', 'DATA': ['03', '22', '%s'%DID[0:2], '%s'%DID[2:], '00', '00', '00', '00']}
        self.ReadResult = self.ReadInternal(seedcmd)
        self.ActualResult = ''
        # 计算出ASCII码
        for i in self.ReadResult[0]['DATA'][5:]:
            num = int(i)-30
            self.ActualResult = self.ActualResult + str(num)
        for i in self.ReadResult[1]['DATA'][1:]:
            num = int(i) - 30
            self.ActualResult = self.ActualResult + str(num)
        self.ExpectResult = str(self.ExpectResult['%s'%DID])
        return (self.ActualResult,self.ExpectResult)

    def close(self):
        self.canMsg.close()

if __name__=='__main__':
    diag = Diagnosis()
    print(diag.ResultProcess_bcd('F1AA'))
    diag.close()

