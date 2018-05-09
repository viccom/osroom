# -*-coding:utf-8-*-
from apps.core.plug_in.manager import plugin_manager

__author__ = 'Allen Woo'
def reader_city(ip):

    '''
    :param reader_obj: reader object
    :param ip:
    :return:a dict
    '''

    # 检测插件
    data = plugin_manager.call_plug(hook_name="ip_geo",
                                    ip=ip)

    if data == "__no_plugin__":
        return {}
    return data