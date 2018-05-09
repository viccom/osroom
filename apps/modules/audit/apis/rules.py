# -*-coding:utf-8-*-
from flask import request
from apps.core.flask.login_manager import osr_login_required

from apps.configs.sys_config import METHOD_WARNING
from apps.core.blueprint import api
from apps.core.flask.permission import permission_required
from apps.core.flask.response import response_format
from apps.modules.audit.process.rules import audit_rules, audit_rule_add, audit_rule_delete
from apps.core.flask.permission import permissions
from apps.core.utils.get_config import get_config

__author__ = 'Allen Woo'
@api.route('/admin/audit/rule/key', methods=['GET'])
@osr_login_required
@permission_required(permissions(["WEB_SETTING"]))
def api_audit_rule_key():

    '''
    GET:
        获取审核规则的所有key与说明, 也就config设置中的audit
        :return:
    '''
    keys = get_config("name_audit", "AUDIT_PROJECT_KEY")
    data = {"keys":keys}
    return response_format(data)

@api.route('/admin/audit/rule', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@osr_login_required
@permission_required(permissions(["WEB_SETTING"]))
def api_audit_rule():
    '''
    GET:
        1. 获取所有验证规则
        project:<str>, "username", "post_category",
        keyword:<str>,不能使用的关键词,支持正则
        page:<int>, 第几页, 默认1
        pre:<int>, 每页返回pre条数据，默认10
        :return:
    POST:
        添加验证规则
        project:<str>, "username", "post_category"
        rule:<str>
        :return:
    DELETE:
        删除规则
        ids:<array>, rule ids
        :return:
    '''
    if request.c_method == "GET":
        data = audit_rules()
    elif request.c_method == "POST":
        data = audit_rule_add()
    elif request.c_method == "DELETE":
        data = audit_rule_delete()
    else:
        data = {"msg_type":"w", "msg":METHOD_WARNING, "http_status":405}
    return response_format(data)