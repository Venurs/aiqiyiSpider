from threading import Thread
import aiqiyiSpider


class SpiderDataThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = "SpiderDataThread"

    def run(self):
        print(self.getName() + "线程启动")
        while True:
            aiqiyiSpider.getCategroyMovieList()
            aiqiyiSpider.getMovieList()
        print(self.getName() + "线程启动")
