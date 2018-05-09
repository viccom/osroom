# -*-coding:utf-8-*-
from flask import url_for
from apps.configs.sys_config import STATIC_PATH
from apps.core.plug_in.manager import plugin_manager
from apps.core.utils.get_config import get_config

__author__ = 'Allen Woo'
def get_localfile_path(file_url_obj):

    '''
    需要提供一个路径的对象
    :param file_url_obj:可以是osroom的路径格式对象, 否则原对象返回
    :return:file url
    '''

    if isinstance(file_url_obj, dict) and "type" in file_url_obj:
        path = "{}/{}/{}".format(STATIC_PATH, get_config("upload", "SAVE_DIR"), file_url_obj["key"]).replace("//", "/")
        return path
    else:
       return file_url_obj

def get_file_url(file_url_obj, save_dir=get_config("upload", "SAVE_DIR")):

    '''
    需要提供一个路径的对象
    :param file_url_obj:可以是osroom的路径格式对象, 否则原对象返回
    :return:file url
    '''

    if isinstance(file_url_obj, dict) and "type" in file_url_obj:

        # 检测上传插件
        data = plugin_manager.call_plug(hook_name="file_storage",
                                        action="get_file_url",
                                        file_url_obj=file_url_obj)
        if data == "__no_plugin__":
            url = url_for('static', filename="{}/{}".format(save_dir, file_url_obj["key"]))
        else:
            url = data
        return url
    else:
        return file_url_obj