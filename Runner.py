import datetime
import logging
import time
import unittest
from HTMLTestRunner import HTMLTestRunner
import gaode_interface
from ddt import data, file_data, unpack, ddt


@ddt
class Gaode(unittest.TestCase):
    def common(self, case, result):
        """
        由于每个case都会执行下面的预期结果和实际结果的比较的代码
        所以单独建一个函数来执行这些比较代码
        """
        actual_status_code, actual_status, actual_info, actual_infocode = result[0], result[1], result[2], result[3]
        # mysql中有的case的状态码是int的，有的是str，此处统一变成int，因为实际结果中就是int类型
        expected_status_code = int(case.get("status_code"))
        # 从excel或mysql中获取expected的结果，
        if isinstance(case.get("expected"), str):
            # 如果是excel中获取case，要将字典格式的字符串转换成字典
            expected = eval(case.get("expected"))
        else:
            # 如果是从mysql中获取的case，本身就是真正的字典，不需要转换
            expected = case.get("expected")

        expected_status = expected["status"]
        expected_info = expected["info"]
        expected_infocode = expected["infocode"]

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_status, expected_status)
        self.assertEqual(actual_info, expected_info)
        self.assertEqual(actual_infocode, expected_infocode)

    @classmethod
    def setUpClass(cls) -> None:
        cls.GaoDe = gaode_interface.GaodeInterface()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    @unittest.skip
    @data(*gaode_interface.load_cases("./cases.xlsx", "Geo"))  # 从excel读取case
    # @data(*gaode_interface.case_from_mysql("interface_cases", "cases_geo"))  # 从mysql中读取case
    def test_01_geo(self, case):
        print("*" * 50, "test_01_geo开始", "*" * 50)
        interface = case["interface"]
        result = self.GaoDe.geo(interface, case)
        self.common(case, result=result)
        print("*" * 50, f"test_01_geo结束", "*" * 50)

    @unittest.skip
    # @data(*gaode_interface.load_cases("./cases.xlsx", "Walking path"))
    @data(*gaode_interface.case_from_mysql("interface_cases", "cases_walking"))  # 从mysql中读取case
    def test_02_walking_path(self, case):
        print("*" * 50, "test_02_geo开始", "*" * 50)
        interface = case["interface"]
        result = self.GaoDe.walking_path(interface, case)
        self.common(case, result=result)
        print("*" * 50, f"test_02_geo结束", "*" * 50)

    # @unittest.skip
    # @data(*gaode_interface.load_cases("./cases.xlsx", "Weather"))
    @data(*gaode_interface.case_from_mysql("interface_cases", "cases_weather"))  # 从mysql中读取case
    def test_03_weather(self, case):
        print("*" * 50, "test_03_geo开始", "*" * 50)
        interface = case["interface"]
        result = self.GaoDe.weather(interface, case)
        self.common(case, result=result)
        print("*" * 50, f"test_03_geo结束", "*" * 50)


if __name__ == '__main__':
    # unittest.main()
    suit = unittest.TestSuite()
    suit.addTest(unittest.TestLoader().loadTestsFromName("Runner.Gaode"))
    nowtime = datetime.datetime.today().strftime("%Y-%m-%d %H.%M.%S")
    file = open(f"./{nowtime}_report.html", "wb")
    runner = HTMLTestRunner(stream=file, verbosity=2, title="高德地图接口测试报告", description="地理编码接口、路径规划接口、天气查询接口")
    runner.run(suit)
