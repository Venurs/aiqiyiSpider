from threading import Thread
import aiqiyiSpider


class SpiderDataThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = "SpiderDataThread"

    def run(self):
        aiqiyiSpider.getCategroyMovieList()
        aiqiyiSpider.getMovieList()
