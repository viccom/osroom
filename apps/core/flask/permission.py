#-*-coding:utf-8-*-
from flask_babel import gettext
from flask_login import current_user
from functools import wraps
from flask import request
from werkzeug.utils import redirect

from apps.app import mdb_sys, redis, cache
from apps.core.flask.response import response_format
from apps.core.utils.get_config import get_config, get_configs
from apps.utils.format.obj_format import json_to_pyseq

__author__ = 'woo'
'''
decorators
'''

def permission_required(permission):
    '''
    权限验证
    :param permission:
    :return:
    '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            custom_per = custom_url_permissions()
            if custom_per:
                r = current_user.can(custom_per)
                keys = " or ".join(get_permission_key(custom_per))
            else:
                r = current_user.can(permission)
                keys = " or ".join(get_permission_key(permission))
            if not r:
                return response_format({"msg":gettext('Permission denied,requires "{}" permission').format(keys),
                        "msg_type":"w", "http_status":401})
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# page url permission required
def page_permission_required():
    '''
    页面路由权限验证
    :return:
    '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            custom_login_required = custom_url_login_auth()
            if custom_login_required and current_user.is_anonymous:
                return redirect(get_config("login_manager", "LOGIN_VIEW"))
            custom_per = custom_url_permissions()
            if custom_per:
                r = current_user.can(custom_per)
                if not r:
                    keys = " or ".join(get_permission_key(custom_per))
                    return response_format({"msg": gettext('Permission denied,requires "{}" permission').format(keys),
                            "msg_type": "w", "http_status": 401})
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def permissions(names):
    '''
    get permissions
    :return:
    '''
    value = 0b0
    for name in names:
        value = value | get_config("permission", name)
    return value

def get_permission_key(permission):

    keys = []
    for k,v in get_configs("permission").items():
        if v & permission:
            keys.append(k)

    return keys


def custom_url_permissions(url=None, method="GET"):

    '''
    获取自定义权限
    :return:
    '''
    if not url:
        url = request.path
        method = request.c_method

    url_per = get_sys_url(url=url.rstrip("/"))
    if url_per and method in url_per["custom_permission"]:
        return url_per["custom_permission"][method]


def custom_url_login_auth(url=None, method="GET"):

    '''
    获取自定义权限
    :return:
    '''
    if not url:
        url = request.path
        method = request.c_method

    url_per = get_sys_url(url=url.rstrip("/"))
    if url_per and url_per["type"]!="page" and method in url_per["login_auth"]:
        return url_per["login_auth"][method]

@cache.cached(timeout=3600, key_base64=False, db_type="redis")
def get_sys_url(url):
    '''
    获取url权限等信息
    :param url:
    :return:
    '''
    value = mdb_sys.db.sys_urls.find_one({"url": url}, {"_id":0})
    return value