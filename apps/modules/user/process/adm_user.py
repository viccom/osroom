# -*-coding:utf-8-*-
from bson.objectid import ObjectId
from flask import request
from flask_babel import gettext
from flask_login import current_user

from apps.core.flask.reqparse import arg_verify
from apps.utils.format.number import get_num_digits
from apps.utils.format.obj_format import json_to_pyseq, str_to_num
from apps.utils.paging.paging import datas_paging
from apps.app import mdb_user
from apps.utils.upload.get_filepath import get_file_url

__author__ = "Allen Woo"


def user():
    id = request.argget.all('id').strip()
    data = {}
    data["user"] = mdb_user.db.user.find_one({"_id": ObjectId(id)})
    if not data["user"]:
        data = {'msg': gettext("The specified user is not found"), 'msg_type': "w", "http_status":404}
    else:
        data["user"]["_id"] = str(data["user"]["_id"])
        data["user"]["role_id"] = str(data["user"]["role_id"])
    return data


def users():
    '''
    Admin获取用户数据
    :return:
    '''
    data = {}
    status = request.argget.all('status')
    page = int(request.argget.all('page', 1))
    pre = int(request.argget.all('pre', 10))
    keyword = request.argget.all('keyword', '').strip()
    query_conditions = {}
    if status == "normal" or not status:
        status = "normal"
        query_conditions = {"is_delete": {"$in": [False, 0]}, "active": {"$in": [True, 1]}}
    elif status == "inactive":
        query_conditions = {"is_delete": {"$in": [False, 0]}, "active": {"$in": [False, 0]}}
    elif status == "cancelled":
        query_conditions = {"is_delete": {"$in": [True, 1]}}

    if keyword:
        keyword = {"$regex":keyword, "$options":"$i"}
        query_conditions["$or"] = [{"username": keyword},
                                   {"email": keyword},
                                   {"custom_domain": keyword}
                                   ]
    us = mdb_user.db.user.find(query_conditions, {"password": 0})
    data_cnt = us.count(True)
    users = list(us.skip(pre * (page - 1)).limit(pre))
    roles = list(mdb_user.db.role.find({}))
    for user in users:
        user['_id'] = str(user['_id'])
        for role in roles:
            if ObjectId(user["role_id"]) == role["_id"]:
                user["role_name"] = role["name"]

        user_login_log = mdb_user.db.user_login_log.find_one({"user_id": user["_id"]}, {"user_id": 0})
        user["user_login_log"] = []
        if user_login_log:
            user_login_log["_id"] = str(user_login_log["_id"])
            user_login_log["login_info"] = sorted(user_login_log["login_info"],
                                                  key=lambda x:x["time"],
                                                  reverse=True)
            user["user_login_log"] = user_login_log

        user_op_log = mdb_user.db.user_op_log.find_one({'user_id': user["_id"]}, {"user_id": 0})
        user["user_op_log"] = []
        if user_op_log:
            user_op_log["_id"] = str(user_op_log["_id"])
            user_op_log["logs"] = sorted(user_op_log["logs"],
                                         key=lambda x:x["time"],
                                         reverse=True)
            user["user_op_log"] = user_op_log


        user["role_id"] = str(user["role_id"])
        user["avatar_url"]["url"] = get_file_url(user["avatar_url"])

    data["users"] = datas_paging(pre=pre, page_num=page, data_cnt=data_cnt, datas=users)
    data["status"] = status
    return data


def user_edit():
    '''
    用户编辑
    :return:
    '''
    id = request.argget.all('id')
    role_id = request.argget.all('role_id')
    active = str_to_num(request.argget.all('active', 0))

    s, r = arg_verify(reqargs=[("id", id), ("role_id", role_id)], required=True)
    if not s:
        return r

    data = {'msg': gettext("Update success"), 'msg_type': "s", "http_status":201}
    update_data = {
        'role_id': role_id,
        'active': active,
    }
    user = mdb_user.db.user.find_one({"_id": ObjectId(id)})
    if user:
        # 权限检查
        current_user_role = mdb_user.db.role.find_one({"_id": ObjectId(current_user.role_id)})
        edit_user_role = mdb_user.db.role.find_one({"_id": ObjectId(user["role_id"])})
        if get_num_digits(current_user_role["permissions"]) <= get_num_digits(edit_user_role["permissions"]):
            # 没有权限修改
            data = {"msg_type": "w", "msg": gettext("No permission modification"), "http_status":401}
            return data

    r = mdb_user.db.user.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if not r.modified_count:
        data = {'msg': gettext("No changes"), 'msg_type': "w", "http_status":201}
    return data


def user_del():
    ids = json_to_pyseq(request.argget.all('ids', []))
    permanent = request.argget.all('permanent', 0)
    try:
        permanent = int(permanent)
    except:
        pass
    noper = 0
    temp_ids = ids[:]
    ids = []
    for i in range(0, len(temp_ids)):
        # 检查是否有权限
        current_user_role = mdb_user.db.role.find_one({"_id": ObjectId(current_user.role_id)})
        rm_user = mdb_user.db.user.find_one({"_id": ObjectId(temp_ids[i])}, {"role_id": 1})
        rm_user_role = mdb_user.db.role.find_one({"_id": ObjectId(rm_user["role_id"])})
        if get_num_digits(current_user_role["permissions"]) <= get_num_digits(rm_user_role["permissions"]):
            # 没有权限删除
            continue
        ids.append(ObjectId(temp_ids[i]))

    if not permanent:
        update_data = {
            'is_delete': 1
        }
        r = mdb_user.db.user.update_many({"_id": {"$in": ids}}, {"$set": update_data})
        if r.modified_count:
            data = {'msg': gettext("Has recovered {} users, {} users can not operate").format(r.modified_count, noper),
                    'msg_type': "s", "http_status":201}
        else:
            data = {'msg': gettext("Recycle user failed.May not have permission"), 'msg_type': "w", "http_status":401}
    else:
        r = mdb_user.db.user.delete_many({"_id": {"$in": ids}, "is_delete": {"$in": [1, True]}})
        if r.deleted_count:
            data = {'msg': gettext(
                "{} users have been deleted and {} users can not be deleted".format(r.deleted_count, noper)),
                    'msg_type': "s", "http_status":204}
        else:
            data = {'msg': gettext("Failed to delete.May not have permission"), 'msg_type': "w", "http_status":401}

    return data


def user_restore():
    ids = json_to_pyseq(request.argget.all('ids', []))
    noper = 0
    re_ids = []
    for i in range(0, len(ids)):
        # 检查是否有权限
        current_user_role = mdb_user.db.role.find_one({"_id": ObjectId(current_user.role_id)})
        re_user = mdb_user.db.user.find_one({"_id": ObjectId(ids[i])}, {"role_id": 1})
        re_user_role = mdb_user.db.role.find_one({"_id": ObjectId(re_user["role_id"])})
        if get_num_digits(current_user_role["permissions"]) <= get_num_digits(re_user_role["permissions"]):
            # 没有权限恢复
            noper += 1
            continue
        re_ids.append(ObjectId(ids[i]))

    update_data = {
        'is_delete': 0
    }

    r = mdb_user.db.user.update_many({"_id": {"$in": re_ids}}, {"$set": update_data})
    if r.modified_count:
        data = {'msg': gettext(
            "Restore the {} users,The other {} users have no power control".format(r.modified_count, noper)),
                'msg_type': "s", "http_status":201}
    else:
        data = {'msg': gettext("Restore the failure.May not have permission"), 'msg_type': "w", "http_status":401}
    return data


def user_activation():
    active = int(request.argget.all('active', 0))
    ids = json_to_pyseq(request.argget.all('ids', []))
    noper = 0
    ac_ids = []
    for i in range(0, len(ids)):
        # 检查是否有权限
        current_user_role = mdb_user.db.role.find_one({"_id": ObjectId(current_user.role_id)})
        re_user = mdb_user.db.user.find_one({"_id": ObjectId(ids[i])}, {"role_id": 1})
        re_user_role = mdb_user.db.role.find_one({"_id": ObjectId(re_user["role_id"])})
        if get_num_digits(current_user_role["permissions"]) <= get_num_digits(re_user_role["permissions"]):
            # 没有权限恢复
            noper += 1
            continue
        ac_ids.append(ObjectId(ids[i]))

    update_data = {
        'active': active
    }

    r = mdb_user.db.user.update_many({"_id": {"$in": ac_ids}}, {"$set": update_data})
    if r.modified_count:
        data = {'msg': gettext(
            "{} user activation is successful, {} no permission to operate".format(r.modified_count, noper)),
                'msg_type': "s", "http_status":201}
    else:
        data = {'msg': gettext("Activation failed.May not have permission"), 'msg_type': "w", "http_status":401}
    return data