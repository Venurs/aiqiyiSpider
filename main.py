from threadUtil import *


if __name__ == '__main__':
    s = SpiderDataThread.SpiderDataThread()
    save = SavaMovieAndPerformerDetailThread.SaveMovieAndPerformerDetailThread()
    d = DownloadImageThread.DownloadImageThread()
    s.start()
    save.start()
    d.start()
    s.join()
    d.join()
    save.join()
