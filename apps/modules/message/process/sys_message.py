# -*-coding:utf-8-*-
from bson import ObjectId
from flask import request
from flask_babel import gettext

from apps.app import mdb_sys
from apps.utils.format.obj_format import str_to_num, objid_to_str, json_to_pyseq
from apps.utils.paging.paging import datas_paging

__author__ = "Allen Woo"

def get_sys_message():

    '''
    管理端获取消息
    :return:
    '''
    data = {}
    ctype = request.argget.all("type")
    status = request.argget.all("status", "normal")
    keyword = request.argget.all("keyword", "")
    pre = str_to_num(request.argget.all("pre", 10))
    page = str_to_num(request.argget.all("page", 1))

    q = {"status":status, "type":ctype}
    if keyword:
        keyword = {"$regex":keyword, "$options":"$i"}
        q["$or"] = [
            {"subject":keyword},
            {"from": keyword},
            {"to": keyword},
            {"body": keyword},
            {"html": keyword},

        ]
    emails = mdb_sys.db.sys_message.find(q)
    data_cnt =  emails.count(True)
    emails = list( emails.sort([("time", -1)]).skip(pre * (page - 1)).limit(pre))
    data["msgs"] = objid_to_str(emails)
    data["msgs"] = datas_paging(pre=pre, page_num=page, data_cnt=data_cnt, datas=data["msgs"])

    return data

def delete_sys_message():

    '''
    删除已发送邮件
    :return:
    '''

    ids = json_to_pyseq(request.argget.all("ids", []))
    for i in range(0, len(ids)):
        ids[i] = ObjectId(ids[i])
    q = {"_id": {"$in": ids}}

    r = mdb_sys.db.sys_message.delete_many(q)
    if r.deleted_count:
        data = {"msg": gettext("Successfully deleted"), "msg_type": "s", "http_status": 204}
    else:
        data = {"msg": gettext("Failed to delete"), "msg_type": "w", "http_status": 400}
    return data

