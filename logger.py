# -*- coding: utf-8 -*-
import logging
import logging.config


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class Logger:
    def __init__(self):
        logging.config.fileConfig("log.conf")
        self.logging = logging.getLogger("file01")

    def get_log(self):
        return self.logging
