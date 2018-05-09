# -*-coding:utf-8-*-
from bson import ObjectId
from flask import request
from flask_babel import gettext
from flask_login import current_user
from werkzeug.exceptions import abort

from apps.core.utils.get_config import get_config
from apps.modules.message.process.user_message import insert_user_msg
from apps.utils.format.obj_format import json_to_pyseq
from apps.core.flask.permission import permissions
from apps.app import mdb_web
from apps.modules.post.process.post_process import get_posts_pr, delete_post, get_post_pr

__author__ = "Allen Woo"

def adm_get_post():

    data = {}
    post_id = request.argget.all('post_id')
    get_post_pr(post_id=post_id, is_admin=True)

    return data


def adm_get_posts():

    page = int(request.argget.all('page', 1))
    pre = int(request.argget.all('pre', 10))
    sort = json_to_pyseq(request.argget.all('sort'))
    status = request.argget.all('status', 'is_issued')
    matching_rec = request.argget.all('matching_rec')
    time_range = int(request.argget.all('time_range', 0))
    keyword = request.argget.all('keyword','').strip()
    fields = json_to_pyseq(request.argget.all('fields'))
    unwanted_fields = json_to_pyseq(request.argget.all('unwanted_fields'))

    # 不能同时使用fields 和 unwanted_fields
    temp_field = {}
    if fields:
        for f in fields:
            temp_field[f] = 1
    elif unwanted_fields:
        for f in unwanted_fields:
            temp_field[f] = 0

    data = get_posts_pr(field=temp_field, page=page, pre=pre, sort=sort, status=status, time_range=time_range, matching_rec=matching_rec,
                      keyword=keyword, is_admin=True)

    return data

def adm_post_audit():

    ids = json_to_pyseq(request.argget.all('ids', []))
    score= int(request.argget.all("score", 0))
    for i in range(0, len(ids)):
        ids[i] = ObjectId(ids[i])
    r = mdb_web.db.post.update_many({"_id":{"$in":ids}},
                               {"$set":{"audited":1, "audit_score":score,
                                        "audit_way":"artificial", "audit_user_id":current_user.str_id}})
    if r.modified_count:
        if score >= get_config("content_inspection", "ALLEGED_ILLEGAL_SCORE"):

            # 审核不通过，给用户通知
            posts = mdb_web.db.post.find({"_id": {"$in": ids}},
                                         {"user_id":1, "title":1, "_id":1, "audit_score":1})
            for p in posts:

                insert_user_msg(user_id=p["user_id"], ctype="notice", label="audit_failure",
                                title=gettext("Post allegedly violated"), content={"text": p["title"]},
                                target_id=str(p["_id"]), target_type="post")


        data = {"msg":gettext("Submitted successfully, {}").format(r.modified_count),
                "msg_type":"s", "http_status":201}
    else:
        data = {"msg":gettext("Submitted failed"), "msg_type":"w", "http_status":400}
    return data


def adm_post_delete():

    data = {}
    ids = json_to_pyseq(request.argget.all('ids', []))
    pending_delete= int(request.argget.all("pending_delete", 1))
    for i in range(0, len(ids)):
        ids[i] = ObjectId(ids[i])
    if pending_delete:
        r = mdb_web.db.post.update_many({"_id":{"$in":ids}},{"$set":{"is_delete":3}})
        if r.modified_count:
            data = {"msg":gettext("Move to a permanently deleted area, {}").format(r.modified_count),
                    "msg_type":"s", "http_status":204}
        else:
            data = {"msg":gettext("No match to relevant data"), "msg_type":"w", "http_status":400}
    else:
        if current_user.can(permissions(["IMPORTANT_DATA_DEL"])):
            data = delete_post(ids=ids)
        else:
            abort(401)

    return data

def adm_post_restore():


    ids = json_to_pyseq(request.argget.all('ids', []))
    for i in range(0, len(ids)):
        ids[i] = ObjectId(ids[i])
    r = mdb_web.db.post.update_many({"_id":{"$in":ids}, "is_delete":3},{"$set":{"is_delete":0}})
    if r.modified_count:
        data = {"msg":gettext("Restore success, {}").format(r.modified_count),
                "msg_type":"s", "http_status":201}
    else:
        data = {"msg":gettext("No match to relevant data"), "msg_type":"w", "http_status":400}

    return data