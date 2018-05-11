# -*-coding:utf-8-*-
from bson.objectid import ObjectId
from flask_babel import gettext
from flask_login import UserMixin, current_user, AnonymousUserMixin
from werkzeug.security import check_password_hash
from apps.core.flask.permission import custom_url_permissions
from apps.utils.upload.get_filepath import get_file_url
from apps.app import mdb_user
from apps.core.utils.get_config import get_config

__author__ = "Allen Woo"

class User(UserMixin):

    def __init__(self, id, **kwargs):
        super(User, self).__init__(**kwargs)
        id = ObjectId(id)
        user = mdb_user.db.user.find_one({"_id":id})
        if user:
            if "password" in user and user["password"]:
                self.no_password = False
                del user["password"]
            else:
                self.no_password = True

            self.id = id
            self.str_id = str(id)
            self.username = user["username"]
            self.email = user["email"]
            self.mphone_num = user["mphone_num"]
            self.custom_domain = user["custom_domain"]
            self.gender = user["gender"]
            self.avatar_url = get_file_url(user["avatar_url"])
            self.role_id = ObjectId(user["role_id"])
            self.active = user["active"]
            self.is_delete = user["is_delete"]
            self.create_at = user["create_at"]
            self.update = user["update_at"]
            self.editor = user["editor"]
            self.jwt_login_time = user.get("jwt_login_time", None)
            if not self.mphone_num:
                user_info_mphone_num = None
            else:
                temp_num = str(self.mphone_num)
                user_info_mphone_num = "{}****{}".format(temp_num[0:3], temp_num[-5:-1]),
            self.user_info = {
                "username":self.username,
                "active":self.active,
                "is_delete":self.is_delete,
                "email":self.email,
                "mphone_num":user_info_mphone_num,
                "custom_domain":self.custom_domain,
                "avatar_url":self.avatar_url,
                "role_id":self.role_id,
                "id":self.id
            }
        else:
            return

    @property
    def password(self):
        raise ArithmeticError(gettext('Password is not a readable attribute'))

    def verify_password(self, password):
        '''
        密码验证
        :param password:
        :return:
        '''
        password_hash = mdb_user.db.user.find_one({'_id':ObjectId(self.id)})["password"]
        return check_password_hash(password_hash, password)

    def can(self, permissions):
        '''
        是否有权限
        :param permissions:
        :return:
        '''
        role = mdb_user.db.role.find_one({"_id":self.role_id})
        return not permissions or (role and int(permissions) & int(role['permissions']) and self.active and not self.is_delete)

    def page_permission_check(self, urls):

        '''
        验证页面路由访问权限
        :param urls: 数组
        :return:
        '''
        for url in urls:
            custom_per = custom_url_permissions(url=url, method="GET")
            if custom_per and current_user.can(custom_per):
                return True
            elif not custom_per:
                return True

    @property
    def is_staff(self):

        role = mdb_user.db.role.find_one({"_id":self.role_id})

        return role and role['permissions'] & get_config("permission", "STAFF")


    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_role_name(self):
        role = mdb_user.db.role.find_one({"_id":self.role_id})
        if role:
            return role["name"]
        return gettext("Unknown")

    def get_id(self):

        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class AnonymousUser(AnonymousUserMixin):

    def __init__(self, **kwargs):
        super(AnonymousUser, self).__init__(**kwargs)

    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None


def insert_op_log(log, user_id=None):
    '''
    插入操作日志
    :param log:
    :param user_id:
    :return:
    '''
    if current_user.is_authenticated:
        user_id = current_user.str_id
    elif user_id:
        user_id = user_id
    else:
        return False
    user_op_log = mdb_user.db.user_op_log.find_one({'user_id':user_id})
    if user_op_log and "logs" in user_op_log:
        logs = user_op_log["logs"]
    else:
        logs = []
    logs.append(log)
    than_num = len(logs) - get_config("weblogger", "USER_OP_LOG_KEEP_NUM")
    if than_num > 0:
        del logs[0:than_num]
    mdb_user.db.user_op_log.update_one({'user_id':user_id},
                                      {"$set":{"logs":logs}},
                                      upsert=True)
