# -*-coding:utf-8-*-
import time
from apps.app import mdb_sys, cache, app
from apps.configs.sys_config import PLUG_IN_CONFIG_CACHE_KEY, CONFIG_CACHE_TIMEOUT

__author__ = "Allen Woo"

def import_plugin_config(plugin_name, config):

    '''
    导入插件配置到数据库
    :param plugin_name 插件名
    :param CONFIG:
    :return:
    '''
    current_time = time.time()
    for k,v in config.items():
        if not "value_type" in v:
            assert Exception('Plugin configuration import database error, missing "value_type"')

        if not "reactivate" in v:
            v["reactivate"] = True
        if not "info" in v:
            v["info"] = ""
        # 查找相同的配置
        r = mdb_sys.db.plugin_config.update_one({"plugin_name":plugin_name,
                                            "key":k,
                                            "value_type":v["value_type"]},
                                            {"$set":{"update_time":current_time,
                                                     "reactivate": v["reactivate"],
                                                     "info":v["info"]}})
        if not r.modified_count:
            # 如果更新时间不成功,此配置不存在数据库
            mdb_sys.db.plugin_config.insert_one({"plugin_name": plugin_name,
                                                 "key": k,
                                                 "value_type": v["value_type"],
                                                 "value":v["value"],
                                                 "reactivate":v["reactivate"],
                                                 "info":v["info"]
                                                 }
                                                )
    # 删除已不需要的配置
    mdb_sys.db.plugin_config.delete_many({"plugin_name": plugin_name,
                                         "update_time": {"$lt":current_time},
                                         })
    # 更新插件配置缓存, # 删除缓存，达到更新缓存
    cache.delete(key=PLUG_IN_CONFIG_CACHE_KEY)

@cache.cached(timeout=CONFIG_CACHE_TIMEOUT, key=PLUG_IN_CONFIG_CACHE_KEY)
def get_all_config():

    '''
    从数据库中查询当前的配置返回
    :return:
    '''
    all_configs = mdb_sys.db.plugin_config.find({})
    configs = {}
    for config in all_configs:
        configs.setdefault(config["plugin_name"], {})
        configs[config["plugin_name"]][config["key"]] = config["value"]
    return configs

def get_plugin_config(plugin_name, key):

    '''
    获取网站动态配置中对应的project中key的值
    :return:
    '''
    with app.app_context():
        return get_all_config()[plugin_name][key]

def get_plugin_configs(plugin_name):
    '''
    获取网站动态配置中对应的project
    :return:
    '''
    with app.app_context():
        return get_all_config()[plugin_name]


