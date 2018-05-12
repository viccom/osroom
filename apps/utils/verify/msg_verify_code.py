#-*-coding:utf-8-*-
import os
import random
from bson import ObjectId
from flask import render_template, url_for
from flask_babel import gettext
import time
from apps.core.blueprint import theme_view, admin_view
from apps.core.plug_in.manager import plugin_manager
from apps.core.template.get_template import get_email_html
from apps.core.template.template import render_absolute_path_template
from apps.utils.send_msg.send_email import send_email
from apps.app import mdb_web
from apps.core.utils.get_config import get_config
from apps.utils.format.time_format import time_to_utcdate
from apps.utils.send_msg.send_message import send_mobile_msg


def _rndChar(i=2):
    '''
    随机数字和字母
    :return:
    '''
    if i == 1:
        # 字母
        an = random.randint(97, 122)
    else:
        # 数字
        an = random.randint(48, 57)
    return chr(an)

def create_code_send(account, account_type):
    '''
    创建email和message验证码
    :param account:
    :param account_type:
    :return:
    '''

    _str = ""
    type = get_config("verify_code", "SEND_CODE_TYPE")
    if type:
        temp_str_list = []
        # 如果存在设置
        if "string" in type and type["string"]:
            for t in range(int(type["string"])):
                c = _rndChar(i=1)
                temp_str_list.append(c)

        if "int" in type and type["int"]:
            for t in range(int(type["int"])):
                c = _rndChar(i=2)
                temp_str_list.append(c)
        # 打乱
        random.shuffle(temp_str_list)
        for c in temp_str_list:
            _str = "{}{}".format(_str, c)

    else:
        for t in range(6):
            i = random.randint(1,2)
            c = _rndChar(i=i)
            _str = "{}{}".format(_str,c)

    if account_type == "email":

        _code = {'str':_str, 'time':time.time(), 'to_email':account, "type":"msg"}
        mdb_web.db.verify_code.insert_one(_code)

        subject = gettext("Verification code")
        data = {"title": subject,
                "body": email_code_html_body(_str),
                "other_info":"",
                }
        html = get_email_html(data)
        send_email(subject=subject,
                   recipients=[account],
                   html_msg=html
                   )
        return {"msg": gettext("Has been sent. If not, please check spam"),
                "msg_type": "s", "http_status": 201}

    elif account_type == "mobile_phone":

        _code = {'str': _str, 'time': time.time(), 'to_tel_number': account, "type": "msg"}
        mdb_web.db.verify_code.insert_one(_code)
        content = gettext("[{}] Your verification code is: {}. "
                          "If you do not send it, please ignore it. "
                          "Please do not tell the verification code to others").format(
                            get_config("site_config", "APP_NAME"), _str)

        s, r = send_mobile_msg([account], content)
        if not s:
            mdb_web.db.verify_code.update_one({"_id":ObjectId(_code['_id'])},
                                              {"$set":{"error":r}})
            return {"msg":r,"msg_type":"w", "http_status":400}

        return {"msg":r, "msg_type":"w", "http_status":201}

def email_code_html_body(code):

    '''
    邮箱验证码正文的html拼接
    :return:
    '''

    body = '''
        <span>{}:</span><br>
        <span style="color: #69B922; font-size: 20px;text-align: center;">
                {}
        </span><br>
        <span>{}</span><br>
        '''.format(gettext('Your verification code is'),code,
               gettext('If you do not send it, please ignore it.Please do not tell the verification code to others'))
    return body

def verify_code(code, email="", tel_number=""):
    '''
    验证email或message验证码
    :param code: 验证码
    :param code:
    :return:
    '''
    r = False
    if not code:
        return r
    _code = None
    if email:
        _code = mdb_web.db.verify_code.find({'to_email':email, "type":"msg"}).sort([("time",-1)]).limit(1)

    elif tel_number:
        _code = mdb_web.db.verify_code.find_one({'to_tel_number': tel_number, "type": "msg"}).sort([("time",-1)]).limit(1)

    if _code and _code.count(True):
        _code = _code[0]
        if _code['str'].lower()==code.lower() \
                and time.time()-_code['time'] < get_config("verify_code", "EXPIRATION"):
            r = True

    return r