from threading import Thread
import aiqiyiSpider
import time


class DownloadImageThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = "DownloadImageThread"

    def run(self):
        # time.sleep(20)
        print(self.getName() + "线程启动")
        while True:
            aiqiyiSpider.downloadPhoto()
        print(self.getName() + "线程任务完成，已结束")
