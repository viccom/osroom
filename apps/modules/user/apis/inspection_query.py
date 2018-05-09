# -*-coding:utf-8-*-
from flask import request
from flask_babel import gettext
from apps.core.flask.login_manager import osr_login_required
from flask_login import current_user
from apps.core.blueprint import api
from apps.app import mdb_user
from apps.core.flask.reqparse import arg_verify
from apps.core.flask.response import response_format

__author__ = 'Allen Woo'

@api.route('/account/data/availability', methods=['GET'])
@osr_login_required
def api_account_data_availability():
    '''
    GET:
        查看用户名，email,个性域是否可以使用
        field:<str>, username or email or custom_domain
        vaule:<str>
        :return:
    '''

    field = request.argget.all('field', 'email').strip()
    value = request.argget.all('value')
    s, r = arg_verify(reqargs=[(field, value)], required=True)
    if not s:
        data = r
    elif mdb_user.db.user.find_one({"_id":{"$ne":current_user.id}, field:value}):
        data = {'msg':gettext("This {} address has been registered").format(field),
                'msg_type':"w", "http_status":403}
    elif mdb_user.db.user.find_one({"_id":current_user.id, field:value}):
        data = {'msg':gettext("This is the email address you currently use".format(field)),
                'msg_type':"w", "http_status":403}
    else:
        data = {'msg':gettext("This {} can be used").format(field),
                'msg_type':"s", "http_status":200}
    return response_format(data)

@api.route('/account/self', methods=['GET'])
@osr_login_required
def api_is_current_user():
    '''
    GET:
        提供一个user id, 获取是否时当前登录用户
        user_id:<str>
        :return:
    '''
    if request.argget.all('user_id') == current_user.str_id:
        data = {'d_msg':gettext("The ID belongs to the current logged in user"),
                'd_msg_type':"s", "is_current_user":True}
    else:
        data = {'d_msg':gettext("The ID belongs to the current logged in user"),
                'd_msg_type':"s", "is_current_user":False}
    return response_format(data)