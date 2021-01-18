from flask import after_this_request
from flask import request
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
        app.config.setdefault('enable', False)
        app.config.setdefault('SHARE_SERVE_LOCAL', False)
        app.config.setdefault("timeout",1)
        
        #app.teardown_request(self.log)
      
        #self.__log()
        self.app.before_request(self.__init_time)
        #def inner():
        self.app.teardown_request(self.__log)

    def __init_time(self):
        self.start = time.time()


    def __log(self, *args):
        print(request.path)
        now = time.time()
        print(now - self.start)
        if self.app.config["timeout"]<= now:
            print("asads")
        # @self.app.before_request
        # def inner():
        #     self.start = time.time()
            
        # print(now-self.start)
        # self.start = now
        #print(request.path)

    def log_entry(self, func):
        # app = self.app or current_app
        @wraps(func)
        def decorator(*args, **kwargs):
            start = time.time()
            # 记录请求开始
            self.app.logger.debug('Start request call: %s' % request.url)
            ret = func(*args, **kwargs)
            # 记录请求结束
            self.app.logger.debug('Finish request call: %s' % request.url)
            duration = time.time() - start
            # 记录请求所耗时长
            self.app.logger.debug('Request: %s consumed %f s' % (request.url, duration))
            return ret

        return decorator