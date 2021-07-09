#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/3 17:06
# @Author  : zhuzhaowen
# @email   : shaowen5011@gmail.com
# @File    : my_async_logging.py
# @Software: PyCharm
# @desc    : "异步记录日志信息"

import threading
from queue import Queue

import os
import logging
from logging.handlers import TimedRotatingFileHandler

class async_logging(threading.Thread):
    LOG_Queue = Queue()

    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "async_logging"

    def run(self):
        while 1:
            data = async_logging.LOG_Queue.get()
            #print(data,data.keys(),)
            loglevel = list(data.keys())[0]
            content = list(data.values())[0]
            #print(loglevel,content)
            getattr(logging, loglevel)(content)


def info(content):
    async_logging.LOG_Queue.put({'info': content})


def error(content):
    async_logging.LOG_Queue.put({'error': content})


def debug(content):
    async_logging.LOG_Queue.put({'debug': content})


def warning(content):
    async_logging.LOG_Queue.put({'warning': content})


def init():
    '''''
        开启写日志的线程
    '''
    print("async_logging init")
    cc = async_logging()
    cc.setDaemon(True)
    cc.start()


if __name__ == "__main__":
    logpath = "./logs/test.log"
    os.makedirs(os.path.dirname(logpath), exist_ok=True)
    logger = logging.getLogger()  # "LazyLogging"
    logger.setLevel(async_logging.info)
    fh = TimedRotatingFileHandler(logpath, when="D", interval=1, backupCount=30)
    datefmt = "%Y-%m-%d %H:%M:%S"
    format_str = '%(asctime)s %(levelname)s %(message)s'
    formatter = logging.Formatter(format_str, datefmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh);async_logging.init()
    init()
    for i in range(517):
        info("sync test {}".format(i))

