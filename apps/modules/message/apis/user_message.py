# -*-coding:utf-8-*-
from flask import request
from apps.core.flask.login_manager import osr_login_required
from apps.configs.sys_config import METHOD_WARNING
from apps.core.blueprint import api
from apps.core.flask.response import response_format
from apps.modules.message.process.user_message import get_user_msgs, update_user_msgs, delete_user_msgs

__author__ = "Allen Woo"

@api.route('/user/message', methods=['GET','PUT', 'DELETE'])
@osr_login_required
def api_user_message():
    '''
    GET:
        获取用户的消息
        type:<array>,消息类型, 比如["notice", "private_letter"]
        label:<array>, 消息label, 默认全部label, 比如['comment', 'audit_failure', 'sys_notice']
        pre:<int>,每页获取几条数据,默认10
        page:<int>,第几页,默认1
        status_update:<str>,获取后的消息状态更新. 可以为: "have_read"
    PUT:
        更新消息状态
        ids:<array>,消息id
        status_update:<str>,获取后的消息状态更新. 可以为: "have_read"
    DELETE:
        删除消息
        ids:<array>,消息id
    :return:
    '''

    if request.c_method == "GET":
        data = get_user_msgs()
    elif request.c_method == "PUT":
        data = update_user_msgs()
    elif request.c_method == "DELETE":
        data = delete_user_msgs()
    else:
        data = {"msg_type":"w", "msg":METHOD_WARNING, "http_status":405}
    return response_format(data)