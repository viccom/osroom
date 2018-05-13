#!/usr/bin/env python
# -*-coding:utf-8-*-
import os
from apps.app import csrf
from apps.core.blueprint import theme_view
from flask import render_template, request, send_file, g
from werkzeug.exceptions import abort
from apps.core.flask.permission import page_permission_required
from apps.core.utils.get_config import get_config
from apps.modules.global_data.process.global_data import get_global_site_data

__author__ = "Allen Woo"

# robots.txt
@csrf.exempt
@theme_view.route('/robots.txt', methods=['GET'])
def robots():
    '''
    robots.txt
    :return:
    '''
    absolute_path = "{}/{}/pages/robots.txt".format(theme_view.template_folder,
                                           get_config("theme", "CURRENT_THEME_NAME"))
    return send_file(absolute_path)

@csrf.exempt
@theme_view.route('/', methods=['GET','POST'])
@page_permission_required()
def index():
    return get_render_template("index")

@csrf.exempt
@theme_view.route('/<path:path>', methods=['GET'])
@page_permission_required()
def pages(path):
    '''
    GET:
        通用视图函数,那些公共的页面将从此进入
        :param path:
        :return:
    '''
    return get_render_template(path.rstrip("/"))

def get_render_template(path):

    '''
    根据路由path,返回一个render_template
    :param path:
    :return:
    '''
    # 拼接当前主题目录
    path = "{}/pages/{}".format(get_config("theme", "CURRENT_THEME_NAME"), path)
    absolute_path = os.path.abspath("{}/{}.html".format(theme_view.template_folder,
                                                        path))
    if not os.path.isfile(absolute_path):
        path = "{}/index".format(path)
        absolute_path = os.path.abspath("{}/{}.html".format(theme_view.template_folder,
                                                                    path))
        if not os.path.isfile(absolute_path):
            abort(404)

    data = dict(request.args)
    for k,v in data.items():
        data[k] = v[0]

    g.site_global = dict(g.site_global, **get_global_site_data(req_type="view"))
    return render_template('{}.html'.format(path), data=data)
