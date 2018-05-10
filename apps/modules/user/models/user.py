# -*-coding:utf-8-*-
import time
from werkzeug.security import generate_password_hash
from apps.core.utils.get_config import get_config

__author__ = 'Allen Woo'


def user_model(**kwargs):

    '''
    Provide parameters, formatted as a dictionary, and then to add some other data to enter.
    提供参数，格式化为一个字典，再将其他一些数据加入进去
    :param kwargs:
    :return:
    '''
    unionid = kwargs.get("unionid")
    if not unionid:
        # 非第三方平台登录注册
        if not kwargs.get("username"):
            return None
        if not kwargs.get("custom_domain"):
            return None
        if not kwargs.get("email") and not kwargs.get("mphone_num"):
            return None

    if not kwargs.get("role_id"):
        return None
    password = kwargs.get("password")
    if password:
        password = generate_password_hash(password)

    active = kwargs.get("active", False)
    user = {
        "username":kwargs.get("username"),
        "custom_domain" :kwargs.get("custom_domain"),
        "password" :password,
        "email" :kwargs.get("email"),
        'gender':'secret',
        'avatar_url': kwargs.get("avatar_url", {"key":None}),
        'address':kwargs.get("address",{}),
        'mphone_num':kwargs.get("mphone_num"),
        'introduction':None,
        'birthday':None,
        "pay":{},
        "editor":get_config("user_model", "EDITOR"),
        "homepage":None,
        "active": active,
        "is_delete": False,
        "role_id": kwargs.get("role_id"),
        "create_at": time.time(),
        "update_at": time.time(),
    }

    if unionid:
        platform_name = kwargs.get("platform_name", "None")
        user["login_platform"] = {platform_name:{"unionid":unionid}}

    return user
