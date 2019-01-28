import logging
import time
from multiprocessing import Process

from .api import app
from .getter import Getter
from .tester import Tester
from .setting import *


class Scheduler:
    def __init__(self):
        self.logger = logging.getLogger('main.scheduler')

    @staticmethod
    def schedule_tester(cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)

    @staticmethod
    def schedule_getter(cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            getter.run()
            time.sleep(cycle)

    @staticmethod
    def schedule_api():
        """
        开启API
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        self.logger.info('代理池开始运行')

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
