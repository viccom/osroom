# -*-coding:utf-8-*-
from flask import request
from flask_babel import gettext

from apps.app import mdb_user
from apps.core.flask.reqparse import arg_verify
from apps.modules.post.process.post_process import get_posts_pr
from apps.utils.format.obj_format import str_to_num
from apps.utils.paging.paging import datas_paging
from apps.utils.upload.get_filepath import get_file_url

__author__ = "Allen Woo"

def search_process():
    '''
    搜索(暂不支持全文搜索)
    只能搜索文章, 用户
    :return:
    '''

    keyword = request.argget.all('keyword')
    target = request.argget.all('target')
    page = str_to_num(request.argget.all('page', 1))
    pre = str_to_num(request.argget.all('pre', 10))

    s, r = arg_verify(reqargs=[(gettext("keyword"), keyword)], required=True)
    if not s:
        return r

    data = {"posts":{}, "users":{}}
    # post
    if not target or target == "post":
        data["posts"] = {}
        data["posts"]["items"] = get_posts_pr(field={"title":1, "issue_time":1, "brief_content":1}, page=page, pre=pre, status="is_issued", sort=None, time_range=None,
                     matching_rec=None, keyword=keyword, other_filter=None, is_admin=False,
                             get_userinfo=False)["posts"]
        data["posts"]["kw"] = keyword

    if not target or target == "user":
        # user
        data["users"] = {"kw": keyword, "items": []}
        query_conditions = {"is_delete": {"$in": [False, 0]}, "active": {"$in": [True, 1]}}
        keyword = {"$regex":keyword, "$options":"$i"}
        query_conditions["$or"] = [{"username": keyword},
                                   {"email": keyword},
                                   {"custom_domain": keyword}
                                   ]
        us = mdb_user.db.user.find(query_conditions,
                                   {"_id": 1, "username":1, "avatar_url":1, "custom_domain":1,
                                    "gender":1, })

        data_cnt = us.count(True)
        users = list(us.skip(pre * (page - 1)).limit(pre))
        for user in users:
            user['_id'] = str(user['_id'])
            user["avatar_url"]["url"] = get_file_url(user["avatar_url"])

        data["users"]["items"] = datas_paging(pre=pre, page_num=page, data_cnt=data_cnt, datas=users)


    return data