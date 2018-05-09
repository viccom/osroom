# -*-coding:utf-8-*-
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from uuid import uuid1
from flask import request, g
from flask_login import current_user
from apps.configs.sys_config import LOG_PATH, WEBLOG_NORMAL_FILENAME, WEBLOG_EXCEP_FILENAME, LOG_FORMATTER, \
    WEBLOG_EXCEP_LEVEL, WEBLOG_NORMAL_LEVEL, WEBLOG_START_FILENAME

__author__ = 'Allen Woo'

class WebLogger():

    def __init__(self):
        self.set_logger = Logger().set_logger

    def init_app(self, app):

        filename = os.path.abspath("{}/{}".format(LOG_PATH, WEBLOG_NORMAL_FILENAME))
        normal_log, handler_normal = self.set_logger(WEBLOG_NORMAL_LEVEL, filename, 'web_normal', LOG_FORMATTER)

        filename = os.path.abspath("{}/{}".format(LOG_PATH, WEBLOG_EXCEP_FILENAME))
        error_log, handler_error = self.set_logger(WEBLOG_EXCEP_LEVEL, filename, 'web_error', LOG_FORMATTER)

        @app.before_request
        def before_request_log():

            '''
            DEFORE REQUEST
            :return:
            '''

            global _weblog_g
            _weblog_g = {"log": {}, "user": current_user}
            st = time.time()
            _weblog_g["log"]['request_id'] = uuid1()  # "{}{}".format(st, randint(1, 1000000))
            g.weblog_id = _weblog_g["log"]['request_id']
            _weblog_g["log"]['st'] = st
            _weblog_g["log"]['ip'] = request.remote_addr
            _weblog_g["log"]['url'] = request.url

            if not _weblog_g["user"].is_anonymous:
                _weblog_g["log"]['user_id'] = _weblog_g["user"].id

        @app.teardown_request
        def teardown_request_log(exception):

            '''
            Teardown request
            :param exception:
            :return:
            '''

            try:
                _weblog_g["log"]["method"] = request.c_method
                _weblog_g["log"]['u_t_m'] = "{} ms".format((time.time() - _weblog_g["log"]['st']) * 1000)
                normal_log.info("[api|view] {}".format(_weblog_g["log"]))
                if exception:
                    error_log.error(_weblog_g["log"])
                    error_log.exception(exception)
            except Exception as e:
                _weblogger_error = {"type": "weblogger error", "exceptione": e}
                error_log.error(_weblogger_error)

    def start_log(self):

        '''
        :return: logger obj
        '''

        filename = os.path.abspath("{}/{}".format(LOG_PATH, WEBLOG_START_FILENAME))
        sys_start_log, handler_start = self.set_logger(set_level=logging.INFO, logfile=filename,
                                                       get_log_name='sys_start', formatter=LOG_FORMATTER)
        return sys_start_log

class Logger():

    def set_logger(self, set_level=logging.INFO,  logfile="{}.log".format(time.time()),
                   get_log_name='logger', formatter='%(asctime)s %(levelname)s %(message)s'):

        if not os.path.exists(os.path.split(logfile)[0]):
            os.makedirs(os.path.split(logfile)[0])

        # 每天保存一个日志, 最多保存7个
        file_handler = TimedRotatingFileHandler(logfile, "midnight", 1, 7)
        file_handler.suffix = "%Y-%m-%d"
        # According to the size
        # file_handler = RotatingFileHandler(filename, maxBytes=10*1024*1024, backupCount=3)
        file_handler.setLevel(set_level)
        _formatter = logging.Formatter(formatter)
        file_handler.setFormatter(_formatter)

        logging.getLogger('{}'.format(get_log_name)).addHandler(file_handler)
        logging.getLogger('{}'.format(get_log_name)).setLevel(logging.INFO)
        logg = logging.getLogger(get_log_name)
        return logg, file_handler

web_start_log = WebLogger().start_log()