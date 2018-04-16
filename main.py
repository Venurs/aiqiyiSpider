from threadUtil import *
import time

if __name__ == '__main__':
    s = SpiderDataThread.SpiderDataThread()
    save = SavaMovieAndPerformerDetailThread.SaveMovieAndPerformerDetailThread()
    d = DownloadImageThread.DownloadImageThread()
    s.start()
    time.sleep(10)
    save.start()
    time.sleep(10)
    d.start()
    s.join()
    d.join()
    save.join()
