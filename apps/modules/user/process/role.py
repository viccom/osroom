# -*-coding:utf-8-*-
from bson import ObjectId
from flask import request
from flask_babel import gettext
from flask_login import current_user

from apps.core.flask.reqparse import arg_verify
from apps.utils.format.number import get_num_digits
from apps.utils.format.obj_format import objid_to_str, json_to_pyseq
from apps.utils.paging.paging import datas_paging
from apps.app import mdb_user
__author__ = "Allen Woo"


def role():

    id = request.argget.all('id').strip()
    data = {}
    data["role"] = mdb_user.db.role.find_one({"_id":ObjectId(id)})
    if not data["role"]:
        data = {'msg':gettext("The specified role is not found"), 'msg_type':"w", "http_status":404}
    else:
        data["role"]["_id"] = str(data["role"]["_id"])

    return data


def roles():
    data = {}
    page = int(request.argget.all('page', 1))
    pre = int(request.argget.all('pre', 10))
    rs = mdb_user.db.role.find({})
    data_cnt = rs.count(True)
    roles = list(rs.skip(pre*(page-1)).limit(pre))
    roles = sorted(roles, key=lambda x:x["permissions"])
    data["roles"] = datas_paging(pre=pre, page_num=page, data_cnt = data_cnt, datas = objid_to_str(roles))
    return data

def add_role():

    name = request.argget.all('name').strip()
    instructions = request.argget.all('instructions').strip()
    default = int(request.argget.all('default', False).strip())
    temp_permissions = json_to_pyseq(request.argget.all('permissions',[]))
    data = {'msg':gettext("Add a success"), 'msg_type':"s", "http_status":201}

    permissions = 0x0
    for i in temp_permissions:
        permissions = permissions | int(i)

    s, r = arg_verify(reqargs=[(gettext("name"), name)], required=True)
    if not s:
       return r
    elif not mdb_user.db.role.find_one({gettext("name"):name}):

        # 权限检查
        user_role = mdb_user.db.role.find_one({"_id":ObjectId(current_user.role_id)})
        if get_num_digits(user_role["permissions"]) <= get_num_digits(permissions):
            data = {"msg":gettext("The current user permissions are lower than the permissions that you want to add,"
                                                  " without permission to add"),
                    "msg_type":"w","http_status":401}
            return data

        if default:
            if not mdb_user.db.role.find_one({"default":{"$in":[1, True]}}):
                mdb_user.db.role.insert_one({"name":name,
                                    "instructions":instructions,
                                    'permissions':permissions,
                                    "default":default})
            else:
                data = {'msg':gettext("Existing default role"), 'msg_type':"w", "http_status":403}
        else:
            mdb_user.db.role.insert_one({"name":name,
                                    "instructions":instructions,
                                    'permissions':permissions,
                                    "default":default})

    else:
        data = {'msg':gettext("Role name already exists"), 'msg_type':"w", "http_status":403}

    return data

def edit_role():

    id = request.argget.all('id').strip()
    name = request.argget.all('name').strip()
    instructions = request.argget.all('instructions').strip()
    default = int(request.argget.all('default', 0))
    temp_permissions = json_to_pyseq(request.argget.all('permissions',[]))

    permissions = 0x0
    for i in temp_permissions:
        permissions = permissions | int(i)

    s, r = arg_verify(reqargs=[(gettext("name"), name)], required=True)
    if not s:
        return r

    data = {"msg": gettext("The current user permissions are lower than the permissions you want to modify,"
                           " without permission to modify"),
            "msg_type": "w", "http_status": 401}
    user_role = mdb_user.db.role.find_one({"_id":ObjectId(current_user.role_id)})
    # 如果当前用户的权限最高位 小于 要修改成的这个角色权重的最高位,是不可以的
    if get_num_digits(user_role["permissions"]) <= get_num_digits(permissions):

        return data

    old_role = mdb_user.db.role.find_one({"_id":ObjectId(id)})
    # 如果当前用户的权限最高位 小于 要修改角色的权限,也是不可以
    if old_role and get_num_digits(old_role["permissions"]) >= get_num_digits(user_role["permissions"]):
        return data

    role = {"name":name,
            "instructions":instructions,
            'permissions':permissions,
            "default":default}

    data = {'msg': gettext("Save success"), 'msg_type': "s", "http_status": 201}
    if not mdb_user.db.role.find_one({"name":name, "_id":{"$ne":ObjectId(id)}}):
        if default:
            if not mdb_user.db.role.find_one({"default":{"$in":[1, True]}, "_id":{"$ne":ObjectId(id)}}):
                r = mdb_user.db.role.update_one({"_id":ObjectId(id)}, {"$set":role})
                if not r.modified_count:
                    data = {'msg':gettext("No changes"), 'msg_type':"w", "http_status":201}
            else:
                data = {'msg':gettext("Existing default role"), 'msg_type':"w", "http_status":403}
        else:
            r = mdb_user.db.role.update_one({"_id":ObjectId(id)}, {"$set":role})
            if not r.modified_count:
                data = {'msg':gettext("No changes"), 'msg_type':"w", "http_status":201}

    else:
        data = {'msg':gettext("Role name already exists"), 'msg_type':"w", "http_status":403}

    return data

def delete_role():

    ids = json_to_pyseq(request.argget.all('ids'))

    user_role = mdb_user.db.role.find_one({"_id":ObjectId(current_user.role_id)})
    noper = 0
    exist_user_role = 0
    for id in ids:
        id = ObjectId(id)
        # 权限检查
        old_role = mdb_user.db.role.find_one({"_id":id})
        # 如果当前用户的权限最高位 小于 要删除角色的权限,也是不可以
        if old_role and get_num_digits(old_role["permissions"]) >= get_num_digits(user_role["permissions"]):
            noper += 1
            continue

        if mdb_user.db.user.find({"role_id":id, "is_delete":{"$in":[0, False, None]}}).count(True):
            exist_user_role += 1
        else:
            mdb_user.db.role.delete_many({"_id":id})
    if not noper:
        data = {'msg':gettext('Delete the success, {} of the roles have users and cannot be deleted').format(exist_user_role),
                'msg_type':'s', "http_status":204}
    else:
        data = {'msg':gettext('{} role do not have permission to delete,'
                              ' {} of the roles have users and cannot be deleted').format(noper, exist_user_role),
                'msg_type':'w', "http_status":400}

    return data