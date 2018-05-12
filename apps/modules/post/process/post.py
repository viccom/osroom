# -*-coding:utf-8-*-
from bson.objectid import ObjectId
from flask import request
from flask_babel import gettext
from flask_login import current_user
from apps.app import mdb_web, mdb_user
from apps.modules.post.process.post_statistical import post_pv
from apps.modules.post.process.post_process import get_posts_pr, get_post_pr
from apps.core.utils.get_config import get_config
from apps.utils.format.obj_format import json_to_pyseq, str_to_num

__author__ = "Allen Woo"

def get_post():

    post_id = request.argget.all('post_id')
    post_pv(post_id)
    data = get_post_pr(post_id=post_id)
    return data

def get_posts():

    page = str_to_num(request.argget.all('page', 1))
    pre = str_to_num(request.argget.all('pre', get_config("post", "NUM_PAGE")))
    sort = json_to_pyseq(request.argget.all('sort'))
    status = request.argget.all('status', 'is_issued')
    matching_rec = request.argget.all('matching_rec')
    time_range = int(request.argget.all('time_range', 0))
    keyword = request.argget.all('keyword','').strip()
    fields = json_to_pyseq(request.argget.all('fields'))
    unwanted_fields = json_to_pyseq(request.argget.all('unwanted_fields'))
    user_id = request.argget.all('user_id')
    category_id = request.argget.all('category_id')

    # 不能同时使用fields 和 unwanted_fields
    temp_field = {}
    if fields:
        for f in fields:
            temp_field[f] = 1
    elif unwanted_fields:
        for f in unwanted_fields:
            temp_field[f] = 0

    other_filter = {}
    if user_id:
        # 获取指定用户的post
        other_filter["user_id"] = user_id

    if category_id:
        try:
            ObjectId(category_id)
            other_filter["category"] = category_id
        except:
            other_filter["category"] = None

    data = get_posts_pr(page=page, field=temp_field, pre=pre, sort=sort, status=status,
                        time_range=time_range,matching_rec=matching_rec, keyword=keyword,
                        other_filter=other_filter)
    return data

def post_like():

    id = request.argget.all('id')
    like = mdb_user.db.user_like.find_one({"user_id":current_user.str_id, "type":"post"})
    if not like:
        user_like = {
            "values":[],
            "type":"post",
            "user_id":current_user.str_id
        }
        mdb_user.db.user_like.insert_one(user_like)
        r1 = mdb_user.db.user_like.update_one({"user_id":current_user.str_id, "type":"post"}, {"$addToSet":{"values":id}})
        r2 = mdb_web.db.post.update_one({"_id":ObjectId(id)}, {"$inc":{"like":1}, "$addToSet": {"like_user_id":current_user.str_id}})

    else:
        if id in like["values"]:
            like["values"].remove(id)
            r2 = mdb_web.db.post.update_one({"_id":ObjectId(id)}, {"$inc":{"like":-1}, "$pull": {"like_user_id":current_user.str_id}})
        else:
            like["values"].append(id)
            r2 = mdb_web.db.post.update_one({"_id":ObjectId(id)}, {"$inc":{"like":1},"$addToSet": {"like_user_id":current_user.str_id}})
        r1 = mdb_user.db.user_like.update_one({"user_id":current_user.str_id, "type":"post"},
                                          {"$set":{"values":like["values"]}})

    if r1.modified_count and r2.modified_count:
        data = {"msg":gettext("Success"), "msg_type":"s", "http_status":201}
    else:
        data = {"msg":gettext("Failed"), "msg_type":"w", "http_status":400}
    return data