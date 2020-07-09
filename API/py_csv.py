#coding:utf-8

import csv
import os

class pyCsv:
    instancesobj = None
    def __init__(self):
        root_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
        self.path = os.path.join(root_path, 'AutoCfg', 'TestCaseCfg.csv')
        self.cfg_dict = {}
        self.open_csv_init()
        pass

    def open_csv_init(self):

        with open(self.path, encoding='GBK')as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                self.cfg_dict[row[1]] = row[2]


    def get_cfgkey_value(self,cfg_key):

        return self.cfg_dict.get(cfg_key)

    @staticmethod
    def get_instances():
        if not pyCsv.instancesobj:
            pyCsv.instancesobj = pyCsv()
        return pyCsv.instancesobj


if __name__ == '__main__':
    cfg = pyCsv.get_instances()