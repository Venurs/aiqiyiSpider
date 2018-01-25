from util import *
class CategroyMovie:
    categroy = ""
    url = ""
    title = ""
    source = ""

    def __init__(self, categroy, url, title, source=None):
        self.categroy = categroy
        self.url = url
        self.title = title
        if source == None:
            self.source = config.SOURCE
        else:
            self.source = source