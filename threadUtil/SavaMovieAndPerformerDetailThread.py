from threading import Thread
import aiqiyiSpider
import time


class SaveMovieAndPerformerDetailThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = "SaveMovieAndPerformerDetailThread(Thread)"

    def run(self):
        time.sleep(20)
        print(self.getName() + "线程启动")
        aiqiyiSpider.getMovieDetail()
        print(self.getName() + "线程任务结束")