# -*-coding:utf-8-*-
from flask import request
from apps.core.blueprint import api
from apps.core.flask.response import response_format
from apps.modules.setting.process.session_set import language_set

__author__ = "Allen Woo"

@api.route('/session/language-set', methods=['PUT'])
def api_language_set():
    '''
    PUT :
        修改当前语言
        language:<str>, 如en_US, zh_CN
    :return:
    '''
    data = language_set()
    return response_format(data)