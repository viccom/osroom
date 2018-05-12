#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask_babel import gettext
from apps.app import csrf, rest_session
from apps.core.auth.rest_token_auth import OsrTokenError
from apps.core.blueprint import api
from apps.core.utils.get_config import get_config
from flask import request, g, session, current_app
from apps.modules.token.process.rest_token import rest_token_auth

__author__ = "Allen Woo"

class Request():

    def all(self, key, default_value=None):
        '''
        所有参数
        :param key: key
        :param d_value: None
        :return:
        '''
        if key in request.values:
            value = request.values[key]
        elif key in request.form:
            value = request.form[key]
        elif request.json and key in request.json:
            value = request.json[key]
        else:
            value = default_value
        return value

    def list(self, key, default_value=None):
        '''
        列表
        :param key: key
        :param d_value: None
        :return:
        '''
        if key in request.values:
            value = request.values.getlist(key)
        elif key in request.form:
            value = request.form.getlist(key)
        elif request.json and key in request.json:
            value = request.json[key]
        else:
            value = default_value
        return value

class OsrRequestProcess():

    '''
    osr请求处理类
    '''
    def __init__(self, **kwargs):
        pass

    def init_request_process(self, app, **kwargs):

        @app.before_request
        def before_request_func():
            '''
            请求前执行函数
            :return:
            '''

            request.c_method = request.method
            if request.path.startswith(api.url_prefix):
                # 只要是api请求都需要token验证

                auth_header = request.headers.get('OSR-RestToken')
                csrf_header = request.headers.get('X-CSRFToken')
                if csrf_header:
                    # 使用CSRF验证
                    csrf.protect()
                elif auth_header:
                    rest_token_auth.auth_rest_token()
                else:
                    response = current_app.make_response(
                        gettext('Token is miss, unconventional web browsing requests please provide "OSR-RestToken",'
                                ' otherwise provide "X-CSRFToken"'))

                    raise OsrTokenError(response.get_data(as_text=True), response=response)

            request.argget = Request()

            '''
            兼容前端某些js框架或浏览器不能使用DELETE, PUT, PATCH等请求时,
            可以在参数中使用_method'
            '''
            if request.argget.all("_method"):
                request.c_method = request.argget.all("_method").upper()
            if not "site_global" in g:
                g.site_global = {}
                g.site_global["language"] = {"all_language": get_config('babel', 'LANGUAGES'),
                                             "current": self.get_current_lang()}

    def init_babel_locale_selector(self, babel):
        '''
        初始化babel locale
        :param babel:
        :return:
        '''
        @babel.localeselector
        def get_locale():
            if not "site_global" in g:
                g.site_global = {}
                g.site_global["language"] = {"all_language": get_config('babel', 'LANGUAGES'),
                                             "current":self.get_current_lang()}
            return g.site_global["language"]["current"]


    def get_current_lang(self):
        '''
        获取当前语言
        :return:
        '''
        lans = list(get_config('babel', 'LANGUAGES').keys())
        if request.headers.get('OSR-RestToken'):
            # RestToken验证请求如果未设置session保存语言, 则使用请求头AcceptLanguges中设置的
            return rest_session.get("language", request.accept_languages.best_match(lans))
        else:
            # 普通浏览器客户端, 获取当session中保存的设置
            return session.get("language", request.accept_languages.best_match(lans))

