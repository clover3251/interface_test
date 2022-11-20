import logging
import os
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


class Log:
    def __init__(self, level='DEBUG'):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)  # 日志器的等级是全局的，和处理器的等级对比 谁高取谁

    def format(self):
        # file_fmt = logging.Formatter("%(filename)s %(lineno)d %(levelname)-10s %(asctime)s---> %(message)s",
        #                              datefmt='%Y-%m-%d %H:%M:%S')
        cons_fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(filename)-s:[%(lineno)-d] --->  %(message)s",
                                     datefmt='%Y-%m-%d %H:%M:%S')
        file_fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(filename)-s:[%(lineno)-d] --->  %(message)s",
                                     datefmt='%Y-%m-%d %H:%M:%S')
        return cons_fmt, file_fmt

    def console_handler(self, level="INFO"):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(self.format()[0])
        self.logger.addHandler(handler)

    def file_handler_debug(self):
        # handler = TimedRotatingFileHandler(
        #     filename="../log/debug/{}_log.txt".format(time.strftime("%Y-%m-%d %H.%M.%S"), time.localtime()))
        if not os.path.exists("../log/debug/"):
            os.makedirs("../log/debug/")
        handler = TimedRotatingFileHandler(filename="../log/debug/debug_log.log", when="midnight")
        handler.setFormatter(self.format()[1])
        self.logger.addHandler(handler)

    def file_handler_info(self, level="INFO"):
        # handler = TimedRotatingFileHandler(filename="../log/info/info_log.log", when="d")
        if not os.path.exists("../log/info/"):
            os.makedirs("../log/info/")
        handler = TimedRotatingFileHandler(filename="../log/info/info_log.log", when="midnight")
        handler.setLevel(level)
        handler.setFormatter(self.format()[1])
        self.logger.addHandler(handler)

    def get_log(self, level="INFO"):
        self.console_handler(level)
        self.file_handler_debug()
        self.file_handler_info(level)
        return self.logger


"""
实例化一个全局的Log对象logger(不用__main__函数)，当其他模块调用此Log模块时，只需要导入此模块 就可以直接使用logger对象，
这样做的目的是：
    1. 当被其他模块导入时，其他模块中不需要重新实例化了
    2. 如果此处将logger对象放到main下面，那么其他模块就调用不了looger对象，因此它们必须重新实例化了
    3. 如果被多个模块导入时，就创建了多个实例化，这会导致每条log消息会被输出多次，也就是创建了几个实例化就会输出几次，换而言之：创建了几个日志器log就会输出几次
        e.g: from x.x.x.logger import my_logging
             logging = my_logging
"""
logger = Log()
my_logging = logger.get_log()

# if __name__ == '__main__':
#     logger = Log()
#     # l = logger.get_log()
#     # l.critical("Critical")
#
#     a = "abc"
#     try:
#         int(a)
#     except Exception as f:
#         # logger.get_log().error(f)
#         logger.get_log().exception(f)
