# utf = "coding-8"
import unittest
from HTMLTestReportCN import HTMLTestRunner
import time, os
from time import sleep
from DiagMain import Diagnosis
from API.Py_excle import pyExcel


class Diagnosis_test(unittest.TestCase):
    def setUp(self):
        self.Diag = Diagnosis()
        self.excel = pyExcel()
        self.ExpectResult = self.excel.can_dict
        self.expandsession = {'ID': '714', 'DATA': ['02', '10', '03', '00', '00', '00', '00', '00']}
        self.refreshsession = {'ID': '714', 'DATA': ['02', '10', '02', '00', '00', '00', '00', '00']}
        self.securt2701 = {'ID': '714', 'DATA': ['02', '27', '01', '00', '00', '00', '00', '00']}
        self.securt2702 = {'ID': '714', 'DATA': ['06', '27', '02', 'cb', '5e', 'a0', 'ba', '00']}

    def test_10_12_1(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '10', '00', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_10_12_2(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '10', '04', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_10_13_1(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '10', '01', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_10_13_2(self):
        seedcmd = {'ID': '714', 'DATA': ['01', '10', '00', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_11_12_1(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '11', '00', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_11_12_2(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '11', '03', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_11_13_1(self):
        seedcmd = {'ID': '714', 'DATA': ['01', '11', '00', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_11_13_2(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '11', '01', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_11_7F_1(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '11', '01', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual('7F', self.ActualResult)

    def test_27_12_1(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '27', '00', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_27_12_2(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '27', '03', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_27_13_1(self):
        seedcmd = {'ID': '714', 'DATA': ['01', '27', '00', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_27_13_2(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '27', '01', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_27_24_1(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '27', '02', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(24, int(self.ActualResult))

    def test_27_24_2(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '27', '0A', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(24, int(self.ActualResult))

    def test_27_35_1(self):
        seedcmd1 = {'ID': '714', 'DATA': ['02', '27', '01', '00', '00', '00', '00', '00']}
        seedcmd2 = {'ID': '714', 'DATA': ['06', '27', '02', '12', '34', '56', '78', '00']}
        seedcmd3 = {'ID': '714', 'DATA': ['06', '27', '02', 'cb', '5e', 'a0', 'ba', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.Diag.ReadInternal(seedcmd3)
        sleep(2)
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.ActualResult = self.Diag.ReadNRC(seedcmd2)
        self.assertEqual(35, int(self.ActualResult))

    def test_27_35_2(self):
        seedcmd1 = {'ID': '714', 'DATA': ['02', '27', '09', '00', '00', '00', '00', '00']}
        seedcmd2 = {'ID': '714', 'DATA': ['06', '27', '0A', '12', '34', '56', '78', '00']}
        seedcmd3 = {'ID': '714', 'DATA': ['06', '27', '0A', '66', '72', '12', '3F', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.Diag.ReadInternal(seedcmd3)
        sleep(2)
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.ActualResult = self.Diag.ReadNRC(seedcmd2)
        self.assertEqual(35, int(self.ActualResult))

    def test_27_36_1(self):
        seedcmd1 = {'ID': '714', 'DATA': ['02', '27', '01', '00', '00', '00', '00', '00']}
        seedcmd2 = {'ID': '714', 'DATA': ['06', '27', '02', '12', '34', '56', '78', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.ActualResult = self.Diag.ReadNRC(seedcmd2)
        self.assertEqual(36, int(self.ActualResult))

    def test_27_36_2(self):
        seedcmd1 = {'ID': '714', 'DATA': ['02', '27', '09', '00', '00', '00', '00', '00']}
        seedcmd2 = {'ID': '714', 'DATA': ['06', '27', '0A', '12', '34', '56', '78', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.ActualResult = self.Diag.ReadNRC(seedcmd2)
        self.assertEqual(36, int(self.ActualResult))

    def test_27_37_1(self):
        seedcmd1 = {'ID': '714', 'DATA': ['02', '27', '01', '00', '00', '00', '00', '00']}
        seedcmd2 = {'ID': '714', 'DATA': ['06', '27', '02', '12', '34', '56', '78', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.Diag.ReadInternal(seedcmd2)
        sleep(2)
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.ActualResult = self.Diag.ReadNRC(seedcmd2)
        self.assertEqual(37, int(self.ActualResult))

    def test_27_37_2(self):
        seedcmd1 = {'ID': '714', 'DATA': ['02', '27', '09', '00', '00', '00', '00', '00']}
        seedcmd2 = {'ID': '714', 'DATA': ['06', '27', '0A', '12', '34', '56', '78', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.Diag.ReadInternal(seedcmd2)
        sleep(2)
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(seedcmd1)
        self.ActualResult = self.Diag.ReadNRC(seedcmd2)
        self.assertEqual(37, int(self.ActualResult))

    def test_27_7F_1(self):
        seedcmd1 = {'ID': '714', 'DATA': ['02', '27', '01', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd1)
        self.assertEqual('7F', self.ActualResult)

    def test_27_7F_2(self):
        seedcmd1 = {'ID': '714', 'DATA': ['02', '27', '09', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd1)
        self.assertEqual('7F', self.ActualResult)

    def test_28_12_1(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '28', '01', '01', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_28_12_2(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '28', '02', '01', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_28_13_1(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '28', '00', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_28_13_2(self):
        seedcmd = {'ID': '714', 'DATA': ['04', '28', '00', '01', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_28_31_1(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '28', '00', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(31, int(self.ActualResult))

    def test_28_31_2(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '28', '00', '04', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(31, int(self.ActualResult))

    def test_28_7F_1(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '28', '00', '01', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual('7F', self.ActualResult)

    def test_28_7F_2(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '28', '00', '01', '00', '00', '00', '00']}
        self.Diag.ReadInternal(self.refreshsession)
        sleep(2)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual('7F', self.ActualResult)

    def test_3E_12_1(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '3E', '01', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_3E_12_2(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '3E', '02', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_3E_13_1(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '3E', '00', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_3E_13_2(self):
        seedcmd = {'ID': '714', 'DATA': ['01', '3E', '00', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_85_12_1(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '85', '00', '00', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_85_12_2(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '85', '03', '01', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_85_13_1(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '85', '00', '01', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_85_7F_1(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '85', '01', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual('7F', self.ActualResult)

    def test_85_7F_2(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '85', '01', '00', '00', '00', '00', '00']}
        self.Diag.ReadInternal(self.refreshsession)
        sleep(2)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual('7F', self.ActualResult)

    def test_14_13_1(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '14', 'FF', 'FF', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_14_13_2(self):
        seedcmd = {'ID': '714', 'DATA': ['05', '14', 'FF', 'FF', 'FF', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_14_31_1(self):
        seedcmd = {'ID': '714', 'DATA': ['04', '14', 'FF', 'FF', 'FE', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(31, int(self.ActualResult))

    def test_14_31_2(self):
        seedcmd = {'ID': '714', 'DATA': ['04', '14', '00', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(31, int(self.ActualResult))

    def test_19_12_1(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '19', '00', 'FF', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_19_12_2(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '19', '03', 'FF', '00', '00', '00', '00']}
        self.Diag.ReadNRC(self.expandsession)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_19_13_1(self):
        seedcmd = {'ID': '714', 'DATA': ['04', '19', '01', 'FF', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_13_2(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '19', '01', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_13_3(self):
        seedcmd = {'ID': '714', 'DATA': ['04', '19', '02', 'FF', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_13_4(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '19', '02', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_13_5(self):
        seedcmd = {'ID': '714', 'DATA': ['04', '19', '0A', 'FF', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_13_6(self):
        seedcmd = {'ID': '714', 'DATA': ['01', '19', '00', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_13_7(self):
        seedcmd = {'ID': '714', 'DATA': ['07', '19', '04', '95', '21', '11', '01', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_13_8(self):
        seedcmd = {'ID': '714', 'DATA': ['05', '19', '04', '95', '21', '11', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_13_9(self):
        seedcmd = {'ID': '714', 'DATA': ['07', '19', '06', '95', '21', '11', '01', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_13_A(self):
        seedcmd = {'ID': '714', 'DATA': ['05', '19', '06', '95', '21', '11', '00', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_19_31_1(self):
        seedcmd = {'ID': '714', 'DATA': ['06', '19', '04', '95', '21', '11', '33', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(31, int(self.ActualResult))

    def test_19_31_2(self):
        seedcmd = {'ID': '714', 'DATA': ['06', '19', '04', '00', '00', '00', '01', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(31, int(self.ActualResult))

    def test_19_31_3(self):
        seedcmd = {'ID': '714', 'DATA': ['06', '19', '06', '00', '00', '00', '01', '00']}
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(31, int(self.ActualResult))

    def test_31_12_1(self):
        seedcmd = {'ID': '714', 'DATA': ['04', '31', '00', 'AF', 'F7', '00', '00', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(self.securt2701)
        self.Diag.ReadInternal(self.securt2702)
        sleep(2)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_31_12_2(self):
        seedcmd = {'ID': '714', 'DATA': ['04', '31', '04', 'AF', 'F7', '00', '00', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(self.securt2701)
        self.Diag.ReadInternal(self.securt2702)
        sleep(2)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(12, int(self.ActualResult))

    def test_31_13_1(self):
        seedcmd = {'ID': '714', 'DATA': ['02', '31', '01', '00', '00', '00', '00', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(self.securt2701)
        self.Diag.ReadInternal(self.securt2702)
        sleep(2)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_31_13_2(self):
        seedcmd = {'ID': '714', 'DATA': ['05', '31', '01', 'AF', 'F7', '00', '00', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(self.securt2701)
        self.Diag.ReadInternal(self.securt2702)
        sleep(2)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(13, int(self.ActualResult))

    def test_31_24_1(self):
        seedcmd = {'ID': '714', 'DATA': ['04', '31', '01', 'AF', 'F7', '00', '00', '00']}
        self.Diag.ReadInternal(self.expandsession)
        self.Diag.ReadInternal(self.securt2701)
        self.Diag.ReadInternal(self.securt2702)
        self.Diag.ReadNRC(seedcmd)
        sleep(5)
        self.ActualResult = self.Diag.ReadNRC(seedcmd)
        self.assertEqual(24, int(self.ActualResult))

    def tearDown(self):
        '''资源释放'''
        self.Diag.close()


if __name__ == '__main__':
    suite = unittest.TestSuite()  # 初始化测试用例集合对象，构建测试套件
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Diagnosis_test))  # 把测试用例加入到测试用力集合中去，将用例加入到检测套件中
    now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
    report_path = os.path.abspath('.') + '\\report\\' + now_time + '_report.html'
    report = open(report_path, mode='wb')
    runner = HTMLTestRunner(stream=report, title='自动化诊断测试报告', description='用例执行情况', verbosity=3,
                            tester='liuxianfeng')  # 定义测试报告
    runner.run(suite)  # 执行测试用例
    report.close()
