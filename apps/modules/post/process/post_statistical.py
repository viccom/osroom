#!/usr/bin/env python
# -*-coding:utf-8-*-
from bson import ObjectId
from flask import request, session
from apps.utils.async.async import async_process
from apps.app import mdb_web

__author__ = "Allen Woo"

@async_process
def post_pv(post_id):
    '''
    记录post的访问量
    :return:
    '''
    mdb_web.init_app(reinit=True)
    sid = request.cookies["session"]
    r = mdb_web.db.access_record.find_one({"post_id":post_id,"sids":sid})
    if not r:
        mdb_web.db.access_record.update_one({"post_id":post_id},
                                       {"$inc":{"pv":1},"$addToSet":{"sids":sid}},
                                      upsert=True)
        mdb_web.db.post.update_one({"_id":ObjectId(post_id)},
                                {"$inc":{"pv":1}})
    else:
        if len(r["sids"]) > 1000:
            mdb_web.db.access_record.update_one({"post_id":post_id},
                                       {"$set":{"sids":[]}})



