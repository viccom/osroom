# -*-coding:utf-8-*-
from flask import request
from apps.core.flask.login_manager import osr_login_required

from apps.configs.sys_config import METHOD_WARNING
from apps.core.blueprint import api
from apps.core.flask.permission import permission_required, permissions
from apps.core.flask.response import response_format
from apps.modules.theme_setting.process.themes import get_themes, switch_theme, upload_theme, delete_theme, \
    get_theme_readme

__author__ = "Allen Woo"

@api.route('/admin/theme', methods=['GET','POST', "PUT", "DELETE"])
@osr_login_required
@permission_required(permissions(["SYS_SETTING"]))
def api_get_themes():
    '''
    主题管理
    GET:
        获取当前所有主题
    POST:
        主题安装
        upfile:<file>, 上传的主题文件
    PUT:
        切换主题
        theme_name:<str>, 主题名称
    DELETE:
        删除主题
        theme_name:<str>, 主题名称
    :return:
    '''

    if request.c_method == "GET":
        if request.argget.all('name'):
            data = get_theme_readme()
        else:
            data = get_themes()

    elif request.c_method == "POST":
        data = upload_theme()

    elif request.c_method == "PUT":
        data = switch_theme()
    elif request.c_method == "DELETE":
        data = delete_theme()
    else:
        data = {"msg_type":"w", "msg":METHOD_WARNING, "http_status":405}
    return response_format(data)