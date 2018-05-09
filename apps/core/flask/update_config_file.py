# -*-coding:utf-8-*-
import json
import time
import regex as re
from copy import deepcopy
from apps.core.logger.web_logging import web_start_log
from apps.utils.format.time_format import time_to_utcdate
from apps.utils.host.get_info import get_host_info
from apps.configs.sys_config import PROJECT_PATH
from apps.configs.config import __readme__, OVERWRITE_DB, CONFIG

__author__ = 'Allen Woo'
now_time = time.time()
host_info = get_host_info()

def update_config_file(mdb_sys, *args, **kwargs):

    '''
    网站启动的时候, 数据库保存的配置-配置文件　同步更新
    config
    mdb_sys
    redis
    '''
    local_config = deepcopy(CONFIG)
    overwrite_db = OVERWRITE_DB
    version_info = mdb_sys.db.sys_config.find_one({"new_version":{"$exists":True}})
    if not version_info:
        now_version = time_to_utcdate(time_stamp=now_time, tformat="%Y_%m_%d_%H_%M_%S")
        version_uses = {"new_version":now_version,
                        "used_versions":[now_version],
                        "update_time":now_time}
        mdb_sys.db.sys_config.insert_one(version_uses)
        web_start_log.info("Initialize the sys_config version info")
    else:
        now_version = version_info["new_version"]

    if version_info and not overwrite_db:
        # 查询当前主机web的的配置版本
        cur_h_version_info = mdb_sys.db.sys_host.find_one({"type":"web",
                                                           "host_info.local_ip":host_info["local_ip"]})
        if not cur_h_version_info:
            cur_h_version_info = {"type":"web", "host_info":host_info,
                                  "conf_version":version_info["new_version"],
                                  "switch_conf_version":None,
                                  "disable_update_conf":0}
            mdb_sys.db.sys_host.insert_one(cur_h_version_info)
            web_start_log.info("Initialize the host version data")

        if cur_h_version_info["switch_conf_version"] or cur_h_version_info["disable_update_conf"]:
            # 数据库配置和本地配置合并:保留本地和数据库的key,用于网站版本回滚
            if cur_h_version_info["switch_conf_version"] and not cur_h_version_info["disable_update_conf"]:
                #　版本切换
                now_version = cur_h_version_info["switch_conf_version"]
            else:
                # 禁止更新
                now_version = cur_h_version_info["conf_version"]
            confs = mdb_sys.db.sys_config.find({"conf_version":now_version})

            if confs.count(True):
                for conf in confs:
                    if not re.search(r"^__.*__$", conf["key"]):
                        if not conf["project"] in local_config:
                            local_config[conf["project"]] = {}

                        if not conf["key"] in local_config[conf["project"]]:
                            local_config[conf["project"]][conf["key"]] = {"value": conf["value"],
                                                                          "type": conf["type"],
                                                                          "info": conf["info"]}
                        else:
                            local_config[conf["project"]][conf["key"]]["value"] = conf["value"]

                web_start_log.info("Config rollback:[db to file] Update version info")
            else:
                web_start_log.error("Config rollback:[db to file] Rollback failure")
                return False
        else:
            # 数据库最新版配置和本地配置合并:以本地配置的key为准,多余的删除
            now_version = version_info["new_version"]
            confs = mdb_sys.db.sys_config.find({"conf_version":now_version})
            if confs.count(True):
                for conf in confs:
                    is_cft = re.search(r"^__.*__$", conf["key"])
                    if not is_cft and conf["project"] in local_config.keys() and conf["key"] in local_config[conf["project"]].keys():
                        local_config[conf["project"]][conf["key"]]["value"] = conf["value"]

                        web_start_log.info("Config merge:[db to file] {} {}".format(conf["project"], conf["key"]))
                    else:
                        mdb_sys.db.sys_config.delete_one({"_id": conf["_id"]})
                        web_start_log.info("Remove the config:{} {}".format(conf["project"], conf["key"]))
            else:
                web_start_log.error("Config merge:[db to file] Merger failure")
                return False

    else:
        web_start_log.info("**Local configuration directly covering the latest edition of the configuration database")


    r = push_to_db(mdb_sys, local_config=deepcopy(local_config), now_version=now_version)
    if not r:
        web_start_log.error("Config update:[file to db] Push failure")
        return False

    # 写配置文件
    info = '''#!/usr/bin/env python\n# -*-coding:utf-8-*-\n__author__ = "Allen Woo"\n'''
    doc = "__readme__='''{}'''\n".format(__readme__)

    # write config.py
    temp_conf = str(json.dumps(local_config, indent=4, ensure_ascii=False))
    wf = open("{}/apps/configs/config.py".format(PROJECT_PATH), "wb")
    wf.write(bytes(info, "utf-8"))
    wf.write(bytes(doc, "utf-8"))
    # 修改配置为同步数据库配置到文件
    wf.write(bytes("# Danger: If True, the database configuration data will be overwritten\n", "utf-8"))
    wf.write(bytes("# 危险:如果为True, 则会把该文件配置覆盖掉数据库中保存的配置\n", "utf-8"))
    wf.write(bytes("OVERWRITE_DB = False\n", "utf-8"))
    wf.write(bytes("CONFIG = ", "utf-8"))
    wf.write(bytes(temp_conf.replace("false", "False").replace("true", "True").replace("null", "None"), "utf-8"))
    wf.close()

    web_start_log.info("Configuration updates and merge is complete")
    return True


def push_to_db(mdb_sys,local_config = None, now_version=None):

    '''
    初始化或者更新配置数据到数据库, 顺便更新CONFIG变量的值
    config:如果为真, 则使用传入的这个配置
    cover: 是否覆盖数据库中的数据
    :return:
    '''

    if not now_version:
        return False

    web_start_log.info("Push to the config version:{}".format(now_version))


    for k,v in local_config.items():
        if not isinstance(v, dict):
            continue

        for k1,v1 in v.items():
            if k1.startswith("__"):
                continue
            try:
                if "__restart__" in v:
                    conf = v1
                    conf["update_time"] = time.time()
                    conf["__restart__"] = v["__restart__"]

                    if "__info__" in v:
                        conf["__info__"] = v["__info__"]
                        
                    if "__sort__" in v:
                        conf["__sort__"] = v["__sort__"]
                    r = mdb_sys.db.sys_config.update_one({"project":k, "key":k1, "conf_version":now_version},
                                                         {"$set":conf}, upsert=True)
                    if r.modified_count or r.upserted_id:
                        web_start_log.info("Config updates: [file to db] {} {}".format(k, k1))
                    elif r.matched_count:
                        web_start_log.info("[file to db] Not updated:{} {}".format(k, k1))
                    else:
                        web_start_log.warning("[file to db] Update failure:{} {}".format(k, k1))
                else:
                    web_start_log.info("[Not import] {} {}".format(k, k1))
            except Exception as e:
                web_start_log.error("[file to db] {}, {} {}".format(e, k, k1))

    # 更新版本信息
    # 将当前版本纳入used_versions, 以便之后管理端修改配置时自动生成新版本
    mdb_sys.db.sys_config.update_one({"new_version": {"$exists": True}, "used_versions":{"$ne":now_version}},
                                     {"$addToSet": {"used_versions": now_version}})

    # 更新主机信息

    host_version = mdb_sys.db.sys_host.find_one({"type":"web", "host_info.local_ip":host_info["local_ip"]})
    up_version = {"conf_version": now_version, "switch_conf_version": None}
    if host_version:
        up_version["host_info"] = host_version["host_info"]
    else:
        up_version["disable_update_conf"] = 0
        host_version["host_info"] = {}

    for k,v in host_info.items():
        up_version["host_info"][k] = v

    if not host_version or not host_version["disable_update_conf"]:
        up_version["start_log"] = "Normal"
        web_start_log.info(up_version["start_log"])
    else:
        up_version["start_log"] = "Update failed. Because there is no open to update"
        web_start_log.warning(up_version["start_log"])

    # 更新主机信息
    mdb_sys.db.sys_host.delete_many({"$or":[{"host_info.local_ip":{"$exists":False}},
                                       {"host_info.local_ip":{"$in":[None, "", False]}}]})

    mdb_sys.db.sys_host.update_one({"type":"web", "host_info.local_ip":host_info["local_ip"]},
                               {"$set":up_version}, upsert=True)

    return True
