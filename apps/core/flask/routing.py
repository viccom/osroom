# -*-coding:utf-8-*-
import time
from werkzeug.routing import BaseConverter
from apps.app import mdb_sys, cache

__author__ = "Allen Woo"

class RegexConverter(BaseConverter):
    '''
    让路由支持正则
    '''
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def push_url_to_db(app):

    '''
    同步url到数据库
    :param app:
    :return:
    '''
    now_time = time.time()
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith("api.") or rule.endpoint.startswith("open_api."):
            type = "api"
        else:
            continue

        r = mdb_sys.dbs["sys_urls"].find_one({"url":rule.rule.rstrip("/")})
        if not r:
            # 不存在
            mdb_sys.dbs["sys_urls"].insert_one({"url": rule.rule.rstrip("/"),
                                                "methods": list(rule.methods),
                                                "endpoint": rule.endpoint,
                                                "custom_permission": {},
                                                "type": type,
                                                "create": "auto",
                                                "update_time": now_time})

        elif r and r["update_time"] < now_time:
            # 如果存在, 并且更新时间比现在前(防止同时启动多个进程时错乱，导致下面程序当旧数据清理)
            mdb_sys.dbs["sys_urls"].update_one({"_id":r["_id"], "update_time":{"$lt":now_time}},
                                               {"$set":{"methods":list(rule.methods),
                                                        "endpoint":rule.endpoint,
                                                        "type":type,
                                                        "create":"auto",
                                                        "update_time":now_time}})

    urls = mdb_sys.dbs["sys_urls"].find({})
    for url in urls:
        if "url" in url:
            cache.delete(key="get_sys_url_url_{}".format(url['url']), db_type="redis")

    # 清理已不存在的api
    mdb_sys.dbs["sys_urls"].delete_many({"type": {"$ne": "page"}, "update_time": {"$lt": now_time}})