# -*-coding:utf-8-*-
from flask import render_template_string

__author__ = 'Allen Woo'


def render_absolute_path_template(path, **context):
    '''
    渲染绝对路径下template文件
    :param path:
    :param context:
    :return:
    '''
    with open(path) as rhtml:
        source = rhtml.read()
    return render_template_string(source=source, **context)


