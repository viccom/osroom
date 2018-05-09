# -*-coding:utf-8-*-
import time

from apps.app import mdb_web, mdb_user, mdb_sys, cache
from apps.core.utils.get_config import get_config

__author__ = "Allen Woo"
@cache.cached(key_base64=False,db_type="mongodb")
def get_post_access():
    '''
    获取文章基本数据统计
    :return:
    '''
    data =  {}
    now_time = time.time()
    s_time = (now_time - 86400 * 6) - now_time % 86400
    data["total"] = mdb_web.db.post.find({}).count(True)
    data["7_total"] = mdb_web.db.post.find({"issue_time":{"$gte":s_time}}).count(True)
    s_time = (now_time - 86400 * 29) - now_time % 86400
    data["30_total"] = mdb_web.db.post.find({"issue_time": {"$gte": s_time}}).count(True)

    data["unaudited"] = mdb_web.db.post.find({"audited": 0,
                                              'is_delete':0,
                                              'issued':1,
                                              "audit_score": {
                                                  "$gte": get_config("content_inspection", "ALLEGED_ILLEGAL_SCORE")}
                                              }).count(True)
    # data["draft"] = mdb_web.db.post.find({"issued": 0, 'is_delete':0}).count(True)
    # data["unqualified"] = mdb_web.db.post.find({"issued": 1, 'is_delete': 0, 'audited':1,
    #                                             'audit_score':{"$lt":get_config("content_inspection",
    #                                                                             "LOWEST_SCORE")}}).count(True)

    return data

@cache.cached(key_base64=False,db_type="mongodb")
def get_comment_access():
    '''
    获取评论基本数据统计
    :return:
    '''
    data = {}
    now_time = time.time()
    s_time = (now_time - 86400 * 6) - now_time % 86400
    data["total"] = mdb_web.db.comment.find({}).count(True)
    data["7_total"] = mdb_web.db.comment.find({"issue_time": {"$gte": s_time}}).count(True)
    s_time = (now_time - 86400 * 29) - now_time % 86400
    data["30_total"] = mdb_web.db.comment.find({"issue_time": {"$gte": s_time}}).count(True)


    data["unaudited"] = mdb_web.db.comment.find({"audited": 0,
                                                 'is_delete': 0,
                                                 'issued': 1,
                                                 "audit_score":{"$gte": get_config("content_inspection", "ALLEGED_ILLEGAL_SCORE")}
                                                 }).count(True)
    # data["unqualified"] = mdb_web.db.comment.find({"issued": 1, 'is_delete': 0, 'audited': 1,
    #                                             'audit_score': {"$lt": get_config("content_inspection",
    #                                                                               "LOWEST_SCORE")}}).count(True)

    return data
@cache.cached(key_base64=False,db_type="mongodb")
def get_user_access():
    '''
    获取用户基本统计数据
    :return:
    '''
    data = {}
    data["total"] = mdb_user.db.user.find({}).count(True)
    now_time = time.time()
    s_time = (now_time - 86400*6) - now_time%86400
    data["7_total"] =  mdb_user.db.user.find({"create_at":{"$gte":s_time}}).count(True)
    s_time = (now_time - 86400 * 29) - now_time % 86400
    data["30_total"] = mdb_user.db.user.find({"create_at": {"$gte": s_time}}).count(True)

    return data

@cache.cached(key_base64=False,db_type="mongodb")
def get_message():
    '''
    获取系统消息数据
    :return:
    '''

    data = {}

    data["email_abnormal"] = mdb_sys.db.sys_message.find({"status": "abnormal", "type":"email"}).count(True)
    data["email_error"] = mdb_sys.db.sys_message.find({"status": "error", "type":"email"}).count(True)

    data["sms_error"] = mdb_sys.db.sys_message.find({"status": "error", "type": "sms"}).count(True)
    data["sms_abnormal"] = mdb_sys.db.sys_message.find({"status": "abnormal", "type": "sms"}).count(True)

    return data

@cache.cached(key_base64=False,db_type="mongodb")
def get_plugin():
    '''
    获取插件数据
    :return:
    '''

    data = {}

    data["plugin_error"] = mdb_sys.db.plugin.find({"error": {"$nin":["",0,False,None]}}).count(True)
    data["plugin_active"] = mdb_sys.db.plugin.find({"active": {"$in":[1, True]}}).count(True)
    data["plugin_total"] = mdb_sys.db.plugin.find({}).count(True)

    return data

@cache.cached(key_base64=False,db_type="mongodb")
def get_media():
    '''
    获取多媒体数据
    :return:
    '''

    data = {}

    data["media_image"] = mdb_web.db.media.find({"type":"image"}).count(True)
    data["media_text"] = mdb_web.db.media.find({"type": "text"}).count(True)
    data["media_video"] = mdb_web.db.media.find({"type": "video"}).count(True)
    data["media_audio"] = mdb_web.db.media.find({"type": "audio"}).count(True)
    data["media_other"] = mdb_web.db.media.find({"type": "other"}).count(True)

    now_time = time.time()
    s_time = (now_time - 86400 * 6) - now_time % 86400
    data["7_total"] = mdb_web.db.media.find({"time": {"$gte": s_time}}).count(True)
    s_time = (now_time - 86400 * 29) - now_time % 86400
    data["30_total"] = mdb_web.db.media.find({"time": {"$gte": s_time}}).count(True)

    return data

@cache.cached(key_base64=False,db_type="mongodb")
def get_inform_data():
    '''
    获取举报数据
    :return:
    '''

    data = {}
    now_time = time.time()
    s_time = (now_time - 86400 * 6) - now_time % 86400
    data["7_post"] = mdb_web.db.post.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["7_comment"] = mdb_web.db.comment.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["7_user"] = mdb_user.db.user.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["7_media"] = mdb_web.db.media.find({"inform.update_time": {"$gte": s_time}}).count(True)

    s_time = now_time - now_time % 86400
    data["1_post"] = mdb_web.db.post.find({"inform.update_time":{"$gte": s_time}}).count(True)
    data["1_comment"] = mdb_web.db.comment.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["1_user"] = mdb_user.db.user.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["1_media"] = mdb_web.db.media.find({"inform.update_time": {"$gte": s_time}}).count(True)

    s_time = now_time - 3600*8
    data["8h_post"] = mdb_web.db.post.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["8h_comment"] = mdb_web.db.comment.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["8h_user"] = mdb_user.db.user.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["8h_media"] = mdb_web.db.media.find({"inform.update_time": {"$gte": s_time}}).count(True)

    s_time = now_time - 3600 * 3
    data["3h_post"] = mdb_web.db.post.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["3h_comment"] = mdb_web.db.comment.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["3h_user"] = mdb_user.db.user.find({"inform.update_time": {"$gte": s_time}}).count(True)
    data["3h_media"] = mdb_web.db.media.find({"inform.update_time": {"$gte": s_time}}).count(True)

    return data