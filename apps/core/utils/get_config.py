# -*-coding:utf-8-*-
from apps.app import cache, mdb_sys, app
from apps.configs.sys_config import CONFIG_CACHE_KEY, CONFIG_CACHE_TIMEOUT

__author__ = 'Allen Woo'
'''
注意:配置有cache,默认CONFIG_TIMEOUT秒过期, 修改配置的程序中保存新后应该删除此cache，让配置立即生效
'''
@cache.cached(timeout=CONFIG_CACHE_TIMEOUT, key=CONFIG_CACHE_KEY)
def get_all_config():

    '''
    从数据库中查询当前的配置返回
    :return:
    '''
    version = mdb_sys.db.sys_config.find_one({"new_version": {"$exists": True}}, {"new_version": 1})
    configs = {}
    if version:
        temp_configs = mdb_sys.db.sys_config.find({"conf_version": version["new_version"]},{"_id":0})
        for config in temp_configs:
            configs.setdefault(config["project"], {})
            configs[config["project"]][config["key"]] = config["value"]
    return configs

def get_config(project, key):

    '''
    获取网站动态配置中对应的project中key的值
    :return:
    '''
    with app.app_context():
        return get_all_config()[project][key]

def get_configs(project):
    '''
    获取网站动态配置中对应的project
    :return:
    '''
    with app.app_context():
        return get_all_config()[project]