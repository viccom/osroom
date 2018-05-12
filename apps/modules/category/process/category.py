# -*-coding:utf-8-*-
import json
from bson import ObjectId
from flask import request
from flask_babel import gettext
from flask_login import current_user

from apps.core.flask.reqparse import arg_verify
from apps.utils.async.async import async_process
from apps.utils.format.obj_format import objid_to_str, json_to_pyseq
from apps.utils.validation.str_format import short_str_verifi
from apps.app import mdb_web
from apps.core.utils.get_config import get_config
__author__ = "Allen Woo"

def get_category_info():

    '''
    获取category信息
    :return:
    '''
    id = request.argget.all('id')
    s, r = arg_verify([(gettext("category id"), id)], required=True)
    if not s:
        return r
    data = {}
    category = mdb_web.db.category.find_one({"_id": ObjectId(id)})
    category["_id"] = str(category["_id"])
    data["category"] = category
    return data


def get_category_type():

    return {"types":get_config("category", "CATEGORY_TYPE")}

def categorys(user_id=None):

    if user_id == None:
        user_id = current_user.str_id
    data = {}
    ntype = request.argget.all('type')
    s, r = arg_verify([(gettext("category type"), ntype)], required=True)
    if not s:
        return r
    category = list(mdb_web.db.category.find({"user_id":user_id, "type":ntype}))
    data["categorys"] = objid_to_str(category, ["_id", "user_id"])
    return data


def category_add(user_id=None):

    if user_id == None:
        user_id = current_user.str_id

    ntype = request.argget.all('type')
    name = request.argget.all('name','')

    s, r = arg_verify([(gettext("category type"), ntype)],
                      only=get_config("category", "CATEGORY_TYPE").values())
    if not s:
        return r
    s1,v = short_str_verifi(name, "class_name")
    s2, r2 = arg_verify(reqargs=[(gettext("name"), name), ], required=True,
                      max_len=int(get_config("category", "CATEGORY_MAX_LEN")))
    if not s1:
        data = {"msg":v, "msg_type":"w", "http_status":422}
    elif not s2:
        data = r2
    elif mdb_web.db.category.find_one({"type":ntype, "user_id":user_id, "name":name}):
        data = {"msg":gettext("Name already exists"), "msg_type":"w", "http_status":403}
    else:
        mdb_web.db.category.insert_one({"type":ntype, "user_id":user_id, "name":name})
        data = {"msg":gettext("Add a success"), "msg_type":"s", "http_status":201}
    return data

def category_edit(user_id=None):

    if user_id == None:
        user_id = current_user.str_id
    id = request.argget.all('id')
    ntype = request.argget.all('type')
    name = request.argget.all('name')

    s1, v = short_str_verifi(name, "class_name")
    s2, r2 = arg_verify(reqargs=[(gettext("name"), name), ], required=True,
                        max_len=int(get_config("category", "CATEGORY_MAX_LEN")))
    if not s1:
        data = {"msg":v, "msg_type":"w", "http_status":422}
    elif not s2:
        data = r2
    elif mdb_web.db.category.find_one({"_id":{"$ne":ObjectId(id)}, "type":ntype, "user_id":user_id, "name":name}):
        data = {"msg":gettext("Name already exists"), "msg_type":"w", "http_status":403}
    else:
        r = mdb_web.db.category.update_one({"_id":ObjectId(id), "user_id":user_id},
                                           {"$set":{"name":name}})
        if r.modified_count:
            update_media_category_name(id, name)
            data = {"msg":gettext("Modify the success"), "msg_type":"s", "http_status":201}
        else:
            data = {"msg": gettext("No modification"), "msg_type": "w", "http_status": 400}
    return data

@async_process
def update_media_category_name(category_id, new_name):
    '''
    更新多媒体与文章category的名称
    '''
    mdb_web.init_app(reinit=True)
    mdb_web.db.media.update_many({"category_id": category_id}, {"$set": {"category": new_name}})

def category_delete(user_id=None):

    if user_id == None:
        user_id = current_user.str_id
    ids = json_to_pyseq(request.argget.all('ids', []))
    if not isinstance(ids, list):
        ids = json.loads(ids)

    for i in range(0, len(ids)):
        ids[i] = ObjectId(ids[i])
    r = mdb_web.db.category.delete_many({"_id":{"$in":ids}, "user_id":user_id})
    if r.deleted_count > 0:
        data = {"msg":gettext("Delete the success,{}").format(r.deleted_count),
                "msg_type":"s", "http_status":204}
    else:
        data = {"msg":gettext("Delete failed"), "msg_type":"w", "http_status":400}
    return data