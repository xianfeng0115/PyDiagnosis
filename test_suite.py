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
        self.ExpectResult=self.excel.can_dict

    def test_ReadF100(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '22', 'F1', '00', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadInternal(seedcmd)
        self.assertEqual(self.ExpectResult['F100'], str(self.ActualResult))

    def test_ReadF110(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '22', 'F1', '10', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadInternal(seedcmd)
        self.assertEqual(self.ExpectResult['F110'], str(self.ActualResult))

    def test_ReadF111_F11F(self):
        for i in range(0,10):
            seedcmd = {'ID': '714', 'DATA': ['03', '22', 'F1', '1%s'%i, '00', '00', '00', '00']}
            self.ActualResult = self.Diag.ReadInternal(seedcmd)
            self.assertEqual(self.ExpectResult['F11%s'%i], str(self.ActualResult))
            sleep(0.5)
        for i in range(ord('A'),ord('F')+1):
            seedcmd = {'ID': '714', 'DATA': ['03', '22', 'F1', '1%s'%chr(i), '00', '00', '00', '00']}
            self.ActualResult = self.Diag.ReadInternal(seedcmd)
            self.assertEqual(self.ExpectResult['F11%s'%chr(i)], str(self.ActualResult))
            sleep(0.5)

    def test_ReadF120_F121(self):
        for i in (0,1):
            seedcmd = {'ID': '714', 'DATA': ['03', '22', 'F1', '2%s'%i, '00', '00', '00', '00']}
            self.ActualResult = self.Diag.ReadInternal(seedcmd)
            self.assertEqual(self.ExpectResult['F12%s'%i], str(self.ActualResult))
            sleep(0.5)

    def test_ReadF183(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '22', 'F1', '83', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadInternal(seedcmd)
        self.assertEqual(self.ExpectResult['F183'], str(self.ActualResult))

    # 零件号：10773535
    def test_ReadF187(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '22', 'F1', '87', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadInternal(seedcmd)
        self.assertEqual(self.ExpectResult['F187'], str(self.ActualResult))

    # 系统供应商标识：545298424
    def test_ReadF18A(self):
        seedcmd = {'ID': '714', 'DATA': ['03', '22', 'F1', '8A', '00', '00', '00', '00']}
        self.ActualResult = self.Diag.ReadInternal(seedcmd)
        self.assertEqual(self.ExpectResult['F18A'], str(self.ActualResult))

    # ECU生产日期和SN：默认全为F由产线写入
    def test_ReadF18B_F18C(self):
        for i in range(ord('B'),ord('C')+1):
            seedcmd = {'ID': '714', 'DATA': ['03', '22', 'F1', '8%s'%chr(i), '00', '00', '00', '00']}
            self.ActualResult = self.Diag.ReadInternal(seedcmd)
            self.assertEqual(self.ExpectResult['F18%s'%chr(i)], str(self.ActualResult))
            sleep(0.5)

    # VIN:默认全为F
    def test_ReadF190(self):
        result = self.Diag.ResultProcess_bcd('F190')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult, self.ActualResult)

    # 版本号比对：只比对前八位[0:8]
    def test_ReadF191(self):
        result = self.Diag.ResultProcess_bcd('F191')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult[0:8], self.ActualResult[0:8])

    def test_ReadF192(self):
        result = self.Diag.ResultProcess_ascii('F192')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult, self.ActualResult)

    def test_ReadF194(self):
        result = self.Diag.ResultProcess_ascii('F194')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult, self.ActualResult)

    # 版本号比对：比对全部22位
    def test_ReadF198(self):
        result = self.Diag.ResultProcess_bcd('F198')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult, self.ActualResult[0:22])
        print(self.ExpectResult, self.ActualResult[0:22])

    def test_ReadF1A0(self):
        result = self.Diag.ResultProcess_bcd('F1A0')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult[0:8], self.ActualResult[0:8])
        print(self.ExpectResult[0:8], self.ActualResult)

    def test_ReadF1A1(self):
        result = self.Diag.ResultProcess_bcd('F1A1')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult, self.ActualResult[0:10])

    def test_ReadF1A2(self):
        result = self.Diag.ResultProcess_bcd('F1A2')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult, self.ActualResult[0:16])
        print(self.ExpectResult, self.ActualResult[0:16])

    def test_ReadF1A5(self):
        result = self.Diag.ResultProcess_bcd('F1A5')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult, self.ActualResult[0:6])
        print(self.ExpectResult, self.ActualResult[0:6])

    def test_ReadF1A8(self):
        result = self.Diag.ResultProcess_bcd('F1A8')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult, self.ActualResult[0:40])
        print(self.ExpectResult, self.ActualResult[0:40])

    def test_ReadF1A9(self):
        result = self.Diag.ResultProcess_bcd('F1A9')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult[0:10], self.ActualResult[0:10])

    def test_ReadF1AA(self):
        result = self.Diag.ResultProcess_bcd('F1AA')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult[0:8], self.ActualResult[0:8])

    def test_ReadF1B5(self):
        result = self.Diag.ResultProcess_bcd('F1B5')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult[0:8], self.ActualResult[0:8])

    def test_ReadF1B6(self):
        result = self.Diag.ResultProcess_bcd('F1B6')
        self.ActualResult = result[0]
        self.ExpectResult = result[1]
        self.assertEqual(self.ExpectResult[0:8], self.ActualResult[0:8])

    def tearDown(self):
        '''资源释放'''
        self.Diag.close()


if __name__ == '__main__':
    suite = unittest.TestSuite()  # 初始化测试用例集合对象，构建测试套件
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Diagnosis_test))  # 把测试用例加入到测试用力集合中去，将用例加入到检测套件中
    now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
    report_path = os.path.abspath('.') + '\\report\\' + now_time + '_report.html'
    report = open(report_path, mode='wb')
    runner = HTMLTestRunner(stream=report, title='自动化诊断测试报告', description='用例执行情况',verbosity=3,tester='liuxianfeng')  # 定义测试报告
    runner.run(suite)  # 执行测试用例
    report.close()