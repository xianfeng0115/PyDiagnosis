import xlrd
import xlwt
import os
import collections

class pyExcel:
    instancesobj = None
    def __init__(self):
        root_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
        self.path = os.path.join(root_path, 'AutoCfg', 'TestCaseCfg.xlsx')
        self.cfg_dict = collections.OrderedDict()
        self.testCaseCfg = collections.OrderedDict()
        self.test5gCaseCfg = collections.OrderedDict()
        self.relay_cfg = []
        self.can_dict = {}
        self.open_csv_init()

        pass

    def open_csv_init(self):
        book = xlrd.open_workbook(self.path)
        sheet = book.sheet_by_name('BaseCfg')
        for line_num in range(1, sheet.nrows):  # iterate 1 to maxrows
            row = sheet.row_values(line_num, 0, end_colx=None)
            ctype = sheet.cell(line_num, 2).ctype
            cell = sheet.cell_value(line_num, 2)
            if ctype == 2 and cell % 1 == 0.0:
                self.cfg_dict[row[1]] = int(row[2])
            else:
                self.cfg_dict[row[1]] = row[2]

        sheet2 = book.sheet_by_name('InterfaceCfg')

        for line_num in range(1, sheet2.nrows):  # iterate 1 to maxrows
            row = sheet2.row_values(line_num, 0, end_colx=None)
            # ctype = sheet2.cell(line_num, 2).ctype
            # cell = sheet2.cell_value(line_num, 2)

            for line in range(0, len(row)):
                ctype = sheet2.cell(line_num, line).ctype
                cell = sheet2.cell_value(line_num, line)
                if line == 0 and cell != '':
                    nextkey = cell
                    self.testCaseCfg[cell] = []
                elif (line == 0 and cell == '') or (line == 1 and cell == ''):
                    pass
                else:
                    self.set_cfg_cell(nextkey, ctype, cell)
        sheet3 = book.sheet_by_name('InterfaceCfg_5G')
        for line_num in range(1, sheet3.nrows):  # iterate 1 to maxrows
            row = sheet3.row_values(line_num, 0, end_colx=None)
            # ctype = sheet2.cell(line_num, 2).ctype
            # cell = sheet2.cell_value(line_num, 2)

            for line in range(0, len(row)):
                ctype = sheet3.cell(line_num, line).ctype
                cell = sheet3.cell_value(line_num, line)
                if line == 0 and cell != '':
                    nextkey = cell
                    self.test5gCaseCfg[cell] = []
                elif (line == 0 and cell == '') or (line == 1 and cell == ''):
                    pass
                else:
                    self.set_cfg_5g_cell(nextkey, ctype, cell)

        sheet4 = book.sheet_by_name('Relay')
        relay_dict = {}
        for line_num in range(1, sheet4.nrows, 2):  # iterate 1 to maxrows
            row = sheet4.row_values(line_num, 0,end_colx=None)

            relay_name = row[2]
            relay_value = int(row[3])
            if row[0] != "" and row[1] != "":
                if relay_dict:
                    self.relay_cfg.append(relay_dict)
                relay_dict = {}
                relay_group_name = row[0]
                relay_port = int(row[1])
                relay_dict["relay_group"] = relay_group_name
                relay_dict[relay_port] = {}
                relay_dict[relay_port][relay_name] = relay_value
            elif row[0] == "" and row[1] != "":
                relay_port = int(row[1])
                relay_dict[relay_port] = {}
                relay_dict[relay_port][relay_name] = relay_value
            else:
                relay_dict[relay_port][relay_name] = relay_value

        self.relay_cfg.append(relay_dict)

        sheet5 = book.sheet_by_name('Diag')
        for line_num in range(1, sheet5.nrows):  # iterate 1 to maxrows
            row = sheet5.cell_value(line_num, 0)
            cell = sheet5.cell_value(line_num, 2)
            self.can_dict[row]=cell

        for line_num in range(1, sheet2.nrows):  # iterate 1 to maxrows
            row = sheet2.row_values(line_num, 0, end_colx=None)
            # ctype = sheet2.cell(line_num, 2).ctype
            # cell = sheet2.cell_value(line_num, 2)

            for line in range(0, len(row)):
                ctype = sheet2.cell(line_num, line).ctype
                cell = sheet2.cell_value(line_num, line)
                if line == 0 and cell != '':
                    nextkey = cell
                    self.testCaseCfg[cell] = []
                elif (line == 0 and cell == '') or (line == 1 and cell == ''):
                    pass
                else:
                    self.set_cfg_cell(nextkey, ctype, cell)


    def set_cfg_cell(self, nextkey, ctype, cell):
        if ctype == 2 and cell % 1 == 0.0:
            self.testCaseCfg[nextkey].append(str(int(cell)))
        else:
            self.testCaseCfg[nextkey].append(cell)

    def set_cfg_5g_cell(self, nextkey, ctype, cell):
        if ctype == 2 and cell % 1 == 0.0:
            self.test5gCaseCfg[nextkey].append(str(int(cell)))
        else:
            self.test5gCaseCfg[nextkey].append(cell)

    def get_cfgkey_value(self,cfg_key):

        return self.cfg_dict.get(cfg_key)

    def get_case_cfg(self, casecfg, *args):
        paraList = self.testCaseCfg.get(casecfg)
        return_type = paraList[0]
        cfgPara = collections.OrderedDict()
        id = 0
        paraName = casecfg
        for index in range(0, len(paraList[1:]), 6):
            paraName = paraList[index+1]
            paraValue = str(paraList[index+2])
            paraType = paraList[index+3]
            paraLen = paraList[index+4]
            threadCount = paraList[index+5]
            processCount = paraList[index + 5]
            if paraLen == '':
                if '*' in str(paraValue):
                    cfgPara[paraName] = self.return_tou(args[id], paraType)
                    id += 1
                else:
                    cfgPara[paraName] = self.return_tou(paraValue, paraType)
            else:
                if '*' in paraValue:
                    cfgPara[paraName] = self.return_tou(args[id], paraType, paraLen)
                    id += 1
                else:
                    cfgPara[paraName] = self.return_tou(paraValue, paraType, paraLen)


        return return_type,threadCount,processCount, cfgPara

    def get_case_5g_cfg(self, casecfg, *args):
        paraList = self.test5gCaseCfg.get(casecfg)
        return_type = paraList[0]
        cfgPara = collections.OrderedDict()
        id = 0
        paraName = casecfg
        for index in range(0, len(paraList[1:]), 7):
            paraName = paraList[index+1]
            paraValue = str(paraList[index+2])
            paraType = paraList[index+3]
            paraLen = paraList[index+4]
            threadCount = paraList[index+5]
            processCount = paraList[index + 6]
            if paraLen == '':
                if '*' in str(paraValue) and '*' == str(paraValue)[0]:
                    cfgPara[paraName] = self.return_tou(args[id], paraType)
                    id += 1
                else:
                    cfgPara[paraName] = self.return_tou(paraValue, paraType)
            else:
                if '*' in paraValue:
                    cfgPara[paraName] = self.return_tou(args[id], paraType, paraLen)
                    id += 1
                else:
                    cfgPara[paraName] = self.return_tou(paraValue, paraType, paraLen)


        return return_type,threadCount,processCount, cfgPara

    def return_tou(self, value, type, paraLen=None, threadCount=1, processCount=1 ):
        if paraLen:
            if type == 'c_int' or type == 'c_uint':
                if '*' in paraLen:
                    return (int(value), type, len(value))
                else:

                    return (int(value), type, int(paraLen))
            else:
                if '*' in paraLen:
                    return (value, type, len(value))
                else:
                    return (value, type, int(paraLen))
        else:
            if (type == 'c_int' or type == 'c_uint') and str(value).isdigit():
                return (int(value), type)
            else:
                return (value, type)

    @staticmethod
    def get_instances():
        if not pyExcel.instancesobj:
            pyExcel.instancesobj = pyExcel()
        return pyExcel.instancesobj


if __name__ == '__main__':
    cfg = pyExcel.get_instances()
    # cfg.get_case_cfg('LibDiasHsmSrvInit', 1)
    pass