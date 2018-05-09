# -*-coding:utf-8-*-
from bson import ObjectId
from flask import request
from flask_babel import gettext
from flask_login import current_user

from apps.app import mdb_sys, cache, mdb_user
from apps.core.flask.reqparse import arg_verify
from apps.utils.format.number import get_num_digits
from apps.utils.format.obj_format import str_to_num, json_to_pyseq
from apps.utils.paging.paging import datas_paging

__author__ = "Allen Woo"

def get_url():

    '''
    获取一个url信息
    :return:
    '''
    id = request.argget.all("id")

    s, r = arg_verify([("id", id)], required=True)
    if not s:
        return r

    url = mdb_sys.db.sys_urls.find_one({"_id":ObjectId(id)})
    if url:
        url["_id"] = str(url["_id"])
        if "OPTIONS" in url["methods"]:
            url["methods"].remove("OPTIONS")
        if "HEAD" in url["methods"]:
            url["methods"].remove("HEAD")
        data = {"url":url}
    else:
        data = {"msg":gettext("No relevant data found"), "msg_type":"w", "http_status":404}
    return data


def get_urls():

    '''
    获取web url
    :return:
    '''
    data = {}
    ctype = request.argget.all("type")
    keyword = request.argget.all("keyword")
    pre = str_to_num(request.argget.all("pre", 10))
    page = str_to_num(request.argget.all("page", 1))
    q = {}
    if ctype:
        q["type"] = ctype
    if keyword:
        keyword = {"$regex":keyword, "$options":"$i"}
        q["$or"] = [{"url":keyword},
                    {"endpoint":keyword},
                    {"custom_permission":keyword},
                    {"methods":keyword}]
    urls = mdb_sys.db.sys_urls.find(q)
    data_cnt = urls.count(True)
    urls = list(urls.sort([("url", 1)]).skip(pre * (page - 1)).limit(pre))
    for url in urls:
        url["_id"] = str(url["_id"])
        if "OPTIONS" in url["methods"]:
            url["methods"].remove("OPTIONS")
        if "HEAD" in url["methods"]:
            url["methods"].remove("HEAD")
        # 判断是否不存在自定义权限
        if not url["custom_permission"]:
            url["custom_permission"] = None
        else:
            no_custom = True
            for v in url["custom_permission"].values():
                if v:
                    no_custom = False
                    break
            if no_custom:
                url["custom_permission"] = None

    data["urls"] = datas_paging(pre=pre, page_num=page, data_cnt=data_cnt, datas=urls)
    return data

def add_url():

    '''
    添加url
    只允许添加页面路由
    :return:
    '''

    url = request.argget.all("url")
    s, r = arg_verify([(gettext("routing"), url)], required=True)
    if not s:
        return r
    url = url.strip()
    if mdb_sys.db.sys_urls.find_one({"url": url}):
        data = {'msg': gettext("Routing already exists"), 'msg_type': "w", "http_status": 403}
    else:
        url_url = {"url": url.rstrip("/"),
                    "methods": ["GET"],
                    "endpoint": "",
                    "custom_permission":{},
                    "type": "page",
                    "create": "manual"}
        r = mdb_sys.db.sys_urls.insert_one(url_url)
        if r.inserted_id:
            data = {"msg": gettext("Added successfully"), "msg_type": "s", "http_status": 201,
                    "inserted_id":str(r.inserted_id)}
        else:
            data = {"msg": gettext("Add failed"), "msg_type": "w", "http_status": 400}
    return data

def update_url():

    '''
    更新修改 url权限
    :return:
    '''
    id = request.argget.all("id")
    method = request.argget.all("method")
    login_auth = str_to_num(request.argget.all("login_auth",0))
    custom_permission = json_to_pyseq(request.argget.all("custom_permission", []))
    s, r = arg_verify([("id", id)], required=True)
    if not s:
        return r

    s, r = arg_verify([(gettext("method"), method)], required=True,
                      only=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
    if not s:
        return r

    permission = 0x0
    for i in custom_permission:
        try:
            i = int(i)
            permission = permission | int(i)
        except:
            pass

    # 修改权限验证
    data = {"msg": gettext("The current user permissions are lower than the permissions you want to modify,"
                           " without permission to modify"),
            "msg_type": "w", "http_status": 401}
    user_role = mdb_user.db.role.find_one({"_id": ObjectId(current_user.role_id)})
    # 如果当前用户的权限最高位 小于 要修改成的权重的最高位,是不可以的
    if get_num_digits(user_role["permissions"]) <= get_num_digits(permission):
        return data

    old_permission = 0
    old_url_per = mdb_sys.db.sys_urls.find_one({"_id":ObjectId(id)})
    if old_url_per and method in old_url_per["custom_permission"]:
        old_permission = old_url_per["custom_permission"][method]

    # 如果当前用户的权限最高位 小于 要修改url请求的权限,也是不可以
    if get_num_digits(user_role["permissions"]) <= get_num_digits(old_permission):
        return data

    r = mdb_sys.db.sys_urls.update_one({"_id":ObjectId(id)},
                                         {"$set":{"custom_permission.{}".format(method):permission,
                                                  "login_auth.{}".format(method):login_auth}})
    if r.modified_count:
        # 清除缓存
        r = mdb_sys.db.sys_urls.find_one({"_id": ObjectId(id)})
        if r:
            cache.delete(key="get_sys_url_url_{}".format(r['url']), db_type="redis")
        data = {"msg":gettext("Modify the success"), "msg_type":"s", "http_status":201}
    else:
        data = {"msg": gettext("No modification"), "msg_type": "w", "http_status": 400}
    return data

def delete_url():

    '''
    删除url, 值允许删除页面路由
    :return:
    '''
    ids = json_to_pyseq(request.argget.all("ids", []))

    for i in range(0, len(ids)):
        ids[i] = ObjectId(ids[i])

    url_pers = list(mdb_sys.db.sys_urls.find({"_id": {"$in": ids}},{"url":1}))
    r = mdb_sys.db.sys_urls.delete_many({"_id":{"$in":ids}, "create":"manual"})
    if r.deleted_count:
        # 清除缓存
        for url_per in url_pers:
            cache.delete(key="get_sys_url_url_{}".format(url_per["url"]), db_type="redis")

        data = {"msg":gettext("Successfully deleted"), "msg_type":"s", "http_status":204}
    else:
        data = {"msg": gettext("Delete failed"), "msg_type": "w", "http_status": 400}
    return data