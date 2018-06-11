# -*- coding: utf-8 -*-

import os
import os.path
import logging
import logging.handlers
import datetime

def create_logger(file):
    # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    if not os.path.exists("logs"):
        os.mkdir("logs")
    fh = logging.handlers.TimedRotatingFileHandler(filename= "logs/" + file + ".log", when="midnight", encoding="utf8")
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def shutdown_logger(logger):
    logging.shutdown()