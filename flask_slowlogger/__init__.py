from flask import after_this_request
from flask import request
from functools import wraps
import logging
import time

class SlowLogger(object):
    def __init__(self,app):
        self.app = app
        self.logger = logging.getLogger("flask-limiter")
        self.enabled = "enabled"
        self.start = 0
        if app is not None:
            self.init_app(app)
        self.start = time.time()

    #提供的默认配置方法，可以在构造工厂中使用
    def init_app(self, app, **kwargs):
        #注册扩展
        app.extensions["slowlogger"] = self
        #设定默认配置文件
        app.config.setdefault('slowlogger_enable', False)
        app.config.setdefault("slowlogger_timeout",1)
  
        self.app.before_request(self.__init_time)
        self.app.teardown_request(self.__log)

    def __init_time(self):
        self.start = time.time()


    def __log(self, *args):
        now = time.time()
        if self.app.config["slowlogger_timeout"]<= now \
                and \
            self.app.config["slowlogger_enable"] == True:
            
            self.app.logger.debug('Request: %s consumed %f s' % (request.url, now-self.start))

    def log_entry(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            start = time.time()
            # 记录请求开始
            self.app.logger.debug(f'Start request call: {request.url}')
            ret = func(*args, **kwargs)
            # 记录请求结束
            self.app.logger.debug(f'Finish request call: {request.url}')
            duration = time.time() - start
            # 记录请求所耗时长
            self.app.logger.debug(f'Request: {request.url} consumed {duration}')
            return ret

        return decorator