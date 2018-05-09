#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import request
from apps.core.flask.login_manager import osr_login_required
import regex as re

from apps.configs.sys_config import METHOD_WARNING
from apps.core.blueprint import api
from apps.core.flask.permission import permission_required, permissions
from apps.core.flask.response import response_format
from apps.modules.user.process.role import role, roles, add_role, edit_role, delete_role
from apps.configs.config import CONFIG

__author__ = "Allen Woo"

@api.route('/admin/role/permission', methods=['GET'])
@osr_login_required
@permission_required(permissions(["USER_MANAGE"]))
def get_role_permissions():
    '''
    GET:
        获取所有的权限表
        :return:
    '''

    data = []
    for k,v in CONFIG["permission"].items():
        if not re.search(r"^__.*__$", k):
            data.append((k,v["value"],v["info"]))
    data = {"permissions":sorted(data, key=lambda x:x[1])}
    return response_format(data)


@api.route('/admin/role', methods=['GET','POST', 'PUT','DELETE'])
@osr_login_required
@permission_required(permissions(["USER_MANAGE"]))
def api_role():
    '''
    GET:
        1. 获取指定ID的角色
        id:<str> ,role id

        2.分页获取全部角色
        page:<int>,第几页，默认第1页
        pre:<int>, 每页查询多少条
    POST:
        添加一个角色
        name:<str>
        instructions:<str>
        default:<int or bool>, 0 or 1
        permissions:<array>, 数组，可以给角色指定多个权重, 如[1, 2, 4, 128]

    PUT:
        修改一个角色
        id:<str>, role id
        name:<str>
        instructions:<str>
        default:<int>, 0 or 1
        permissions:<array>, 数组，可以给角色指定多个权重, 如[1, 2, 4, 128]

    DELETE:
        删除角色
        ids:<arry>, role ids
    '''

    if request.c_method == "GET":
        if request.argget.all('id'):
            data = role()
        else:
            data = roles()

    elif request.c_method == "POST":
        data = add_role()

    elif request.c_method == "PUT":
        data = edit_role()

    elif request.c_method == "DELETE":
        data = delete_role()

    else:
        data = {"msg_type":"w", "msg":METHOD_WARNING, "http_status":405}
    return response_format(data)