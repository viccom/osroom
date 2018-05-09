#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import request
from apps.core.flask.login_manager import osr_login_required

from apps.configs.sys_config import METHOD_WARNING
from apps.core.blueprint import api
from apps.core.flask.permission import permission_required
from apps.core.flask.response import response_format
from apps.modules.setting.process.host_setting import get_sys_host, sys_host_edit, \
    sys_host_delete, sys_host_exec_cmd, sys_host_connect_test
from apps.core.flask.permission import permissions

__author__ = "Allen Woo"
@api.route('/admin/setting/sys/host', methods=['GET', 'POST', 'PUT', 'DELETE'])
@osr_login_required
@permission_required(permissions(["SYS_SETTING"]))
def api_sys_host():

    '''
    GET:
        获取主机的信息
        ip:<str>,要获取哪个主机的日志
        :return:

    PUT:
        设置主机连接信息与重启命令
        username:<str>,主机用户名
        password:<str>,主机密码
        host_ip:<str>,要获取哪个主机的日志
        host_port:<int>,主机端口
        cmd:<str>, 命令, 注释使用#

    '''

    if request.c_method == "GET":
        data = get_sys_host()
    elif request.c_method == "PUT":
        data = sys_host_edit()
    elif request.c_method == "DELETE":
        data = sys_host_delete()
    else:
        data = {"msg_type":"w", "msg":METHOD_WARNING, "http_status":405}
    return response_format(data)

@api.route('/admin/setting/sys/host/cmd-execute', methods=['PUT'])
@osr_login_required
@permission_required(permissions(["SYS_SETTING"]))
def sys_host_cmd_exec():

    '''
    PUT:
        命令执行
        host_ip:<str>
        cmd:<str>, 要执行的Linux 命令,如果没有则自动执行主机保存的常用命令
    :return:
    '''

    data = sys_host_exec_cmd()
    return response_format(data)

@api.route('/admin/setting/sys/host/connection-test', methods=['PUT'])
@osr_login_required
@permission_required(permissions(["SYS_SETTING"]))
def sys_host_connection_test():

    '''
    PUT:
        服务器连接测试
        host_ip:<str>
    :return:
    '''

    data = sys_host_connect_test()
    return response_format(data)
