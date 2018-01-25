from util import config
from hashlib import md5
class Movie:
    moviename = ""
    time = ""
    url = ""
    imagepath = ""
    saveimagepath = ""
    score = ""
    status = ""
    source = ""

    def __init__(self, moviename, time, url, imagepath, score, status=None, source=config.SOURCE):
        self.moviename = moviename
        self.time = time
        self.url = url
        self.imagepath = imagepath
        self.saveimagepath = config.PHOTOSAVEPATH + makeMd5(imagepath) + ".jpg"
        self.score = score
        self.status = status
        self.source = source


def makeMd5(path):
    m = md5()
    m.update(path.encode("utf-8"))
    return m.hexdigest()