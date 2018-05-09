# -*-coding:utf-8-*-
from flask import request
from flask_babel import gettext
from flask_login import current_user, logout_user
import time
from werkzeug.security import generate_password_hash
from apps.core.template.get_template import get_email_html
from apps.core.utils.get_config import get_config
from apps.utils.send_msg.send_email import send_email
from apps.utils.validation.str_format import password_format_ver, email_format_ver
from apps.utils.verify.msg_verify_code import verify_code
from apps.app import mdb_user
from apps.modules.user.process.user import insert_op_log

__author__ = "Allen Woo"
def account_password_reset():

    now_pass = request.argget.all('now_password').strip()
    pass1 = request.argget.all('password').strip()
    pass2 = request.argget.all('password2').strip()
    if not now_pass:
        data = {'msg':gettext("Now use the password mistake"), 'msg_type':"w", "http_status":401}
        return data
    elif pass1 != pass2:
        data = {'msg':gettext("Two password is not the same"), 'msg_type':"w", "http_status":400}
    else:
        data = p_password_reset(now_pass, pass1)
    return data

def account_password_retrieve():

    code = request.argget.all('email_code')
    email = request.argget.all('email')
    password = request.argget.all('password')
    password2 = request.argget.all('password2')

    if password != password2:
       data= {'msg':'Two password is not the same', "msg_type":"w", "http_status":400}
    else:
       data= p_retrieve_password(email, code, password, password2)

    # 验证码
    #_code = create_code_send(email)
    #data['code'] = _code
    return data


def p_password_reset(old_pass, new_pass):

    '''
    用户密码修改
    :param old_pass:
    :param new_pass:
    :return:
    '''

    r,s = password_format_ver(new_pass)
    if not r:
        data= {"msg_type":"w", "msg":s, "http_status":400}
        return data

    if current_user.verify_password(old_pass) or current_user.no_password:
        password_hash = generate_password_hash(new_pass)
        # 将jwt_login_time设为{}退出所有jwt登录的用户
        r = mdb_user.db.user.update_one({"_id":current_user.id},
                                        {"$set":{"password":password_hash,
                                                 "jwt_login_time":{}}})
        if r.modified_count:
            oplog = {
                   'op_type':'set_password',
                   'time':time.time(),
                   'status':'s',
                   'info':'',
                   'ip':request.remote_addr
                   }
            insert_op_log(oplog)
            data = {"msg_type":"s","msg":gettext("Password change is successful, please login again"),
                "http_status": 201}
            logout_user()
            data['to_url'] = get_config("login_manager", "LOGIN_VIEW")

        else:
            data = {
                "msg_type": "w","msg": gettext("Password change failed(unknown error)"), "http_status":400}
        return data

    data = {
             "msg_type":"e","http_status":400,
             "msg":gettext("Now use the password mistake")}

    return data

def p_retrieve_password(email, code, password, password2):
    '''
    密码重设
    :param account:
    :param code:
    :param password:
    :param password2:
    :return:
    '''

    data = {}
    if not email:
        data = {'msg':gettext('Account does not exist'), 'msg_type': 'e', "http_status": 404}
        return data

    s,r = email_format_ver(email=email)
    if s:
        user = mdb_user.db.user.find_one({"email":email})
    else:
        data = {"msg":r, "msg_type":"e", "http_status":"403"}
        return data

    if user:
        r = verify_code(code, email=user["email"])
    else:
        data = {'msg':gettext('Account does not exist'), 'msg_type':'e', "http_status":404}
        return data

    if not r:
        data = {'msg':gettext('Email or SMS verification code error'),
                'msg_type':'e', "http_status":401}
    else:
        if user:
            r = password_format_ver(password)
            if not r:
                data = {"msg": r, "msg_type": "e", "http_status": "403"}
                return data
            elif password != password2:
                data = {'msg':gettext('Two password is not the same'),
                        'msg_type':'w', "http_status":400}
            else:
                password_hash = generate_password_hash(password)
                # 将jwt_login_time设为{}退出所有jwt登录的用户
                r = mdb_user.db.user.update_one({"_id": user["_id"]},
                                                {"$set": {"password": password_hash,
                                                          "jwt_login_time": {}}})
                if r.modified_count:
                    oplog = {
                               'op_type':'retrieve_pass',
                               'time':time.time(),
                               'status':'s',
                               'info':'',
                               'ip':request.remote_addr
                               }
                    insert_op_log(oplog, user_id=user["_id"])

                    # 发送邮件
                    subject = gettext("Password reset notification")
                    body = "Your account <a>{}</a> has reset your password. <br>Please keep it safe.".format(user["email"])
                    data = {"title": subject,
                            "body": body,
                            "other_info": gettext("End"),
                            }
                    html = get_email_html(data)

                    send_email(subject=subject,
                               recipients=[user["email"]],
                               html_msg=html)
                    data = {'msg':gettext('Password reset successfully.Please return to login page to login'),'msg_type':'s', "http_status":201}
                    logout_user()
                else:
                    data = {"msg_type": "w", "msg": gettext("Reset password failed(unknown error)"),
                            "http_status": 400}
                return data
    return data