# -*-coding:utf-8-*-
import os

import shutil
from flask import request
import regex as re
from flask_babel import gettext

from apps.app import mdb_sys
from apps.configs.sys_config import THEME_TEMPLATE_FOLDER
from apps.core.flask.reqparse import arg_verify
from apps.core.utils.get_config import get_config

__author__ = "Allen Woo"

def add_page():

    routing = request.argget.all('routing')
    content = request.argget.all('content', "")
    ctype = request.argget.all('type', 'html')

    s, r = arg_verify(reqargs=[(gettext("file type"), ctype)], only=["html"],
                      required=True)
    if not s:
        return r
    if ctype == "html":
        dirname = "pages"
    else:
        dirname = "static"

    regex_filter = r"(osr/|osr-admin/)"
    s, r = arg_verify(reqargs=[(gettext("routing"), routing)], required=True)
    if not s:
        data = r
    elif re.search(regex_filter, routing):
        data = {"msg":gettext("This route can not be used"), "msg_type":"w",
                "http_status":403}
    else:
        filename = os.path.split(routing)[-1]
        path = "{}/{}/{}/{}".format(THEME_TEMPLATE_FOLDER, get_config("theme", "CURRENT_THEME_NAME"),
                                    dirname, os.path.split(routing)[0]).replace("//", "/")

        # 是否存在同名的目录
        relative_path = "{}/{}".format(path, filename)
        if os.path.exists(relative_path):
            data = {"msg":gettext("This route can not be used"), "msg_type":"w",
                "http_status":403}
            return data

        # 是否存在同名的html文件
        file = "{}/{}.{}".format(path, filename, ctype)
        if os.path.exists(file):
            data = {"msg":gettext("Routing existing"), "msg_type":"w",
                "http_status":403}
            return data

        if not os.path.exists(path):
            os.makedirs(path)
        with open(file, "w") as wf:
            wf.write(content)

        # 记录
        mdb_sys.db.theme.update_one({"theme_name": get_config("theme", "CURRENT_THEME_NAME")},
                                    {"$addToSet":{"custom_pages":"{}.{}".format(filename, ctype)}},
                                    upsert=True)


        data = {"msg":gettext("Added successfully"), "msg_type":"s",
                "http_status":201, "url":"/{}".format(routing.strip("/"))}
    return data

def delete_page():

    '''
    删除再管理端自定义页面
    :return:
    '''

    filename = request.argget.all('filename', "index").strip("/")
    file_path = request.argget.all('file_path', "").strip("/")

    path = os.path.join(THEME_TEMPLATE_FOLDER, get_config("theme", "CURRENT_THEME_NAME"))
    file_path = "{}/{}".format(path, file_path)
    file = os.path.join(file_path, filename)
    if not os.path.exists(file):
        mdb_sys.db.theme.update_one({"theme_name": get_config("theme", "CURRENT_THEME_NAME")},
                                    {"$pull": {"custom_pages": filename}})

        data = {"msg": gettext("File not found,'{}'").format(file),
                "msg_type": "w", "http_status": 404}
    else:

        custom = mdb_sys.db.theme.find_one({"theme_name": get_config("theme", "CURRENT_THEME_NAME"),
                                   "custom_pages":filename})
        if custom:
            os.remove(file)
            mdb_sys.db.theme.update_one({"theme_name": get_config("theme", "CURRENT_THEME_NAME")},
                                        {"$pull": {"custom_pages": filename}})
            if not os.listdir(file_path):
                shutil.rmtree(file_path)
            data = {"msg": gettext("Successfully deleted"), "msg_type": "s",
                    "http_status": 204}
        else:
            data = {"msg": gettext("This file can not be deleted"), "msg_type": "w",
                    "http_status": 403}
    return data