# -*-coding:utf-8-*-
from flask_login import current_user
import regex as re
from flask_babel import gettext
from apps.app import mdb_sys
from apps.core.flask.reqparse import arg_verify

__author__ = 'Allen Woo'

def ver_name(name, project=None):

    '''
    各种名字字符验证
    Character name to verify
    :param name:
    :return:
    '''

    s, r = arg_verify(reqargs=[(gettext("name"),name)], required=True)
    if not s:
        return False, r["msg"]

    elif re.search(r"[\.\*#\?]+",name):
        return False, gettext("The name format is not correct,You can't use '.','*','#','?'")
    elif current_user.is_authenticated and current_user.is_staff:
        return True, gettext("")

    if project:
        rules = mdb_sys.db.audit_rules.find({"project":project})
        for rule in rules:
            if re.search(r"^{}$".format(rule["rule"]), name):
                return False, gettext("Name is not legal, there is sensitive information")
    return True, gettext("")


def ver_user_domainhacks(domain):

    '''
    用户个性域名验证
    Character name to verify
    :param name:
    :return:
    '''
    s, r = arg_verify(reqargs=[(gettext("custom domain"), domain)], required=True)
    if not s:
        return False, r["msg"]
    if not re.search(r"[0-9a-zA-Z]{4}", domain):
        return False, gettext("The domain format is not correct,Only use Numbers, letters, and at least 4 characters")
    else:
        return True, gettext("")

def email_format_ver(email):

    '''
    邮箱字符验证
    Character email to verify
    :param email:
    :return:
    '''

    if re.search(r"^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$",email):
        return True, ""
    else:
        return False, gettext("The email format is not correct")

def mobile_phone_format_ver(number):

    '''
    邮箱字符验证
    Character email to verify
    :param email:
    :return:
    '''

    if re.search(r"^[0-9]{11}$", number):
        return True, ""
    else:
        return False, gettext("The email format is not correct")

def url_format_ver(url):

    if re.search(r"(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?", url):
        return True, ""
    else:
        return False, gettext("The url format is not correct")


def password_format_ver(password):

    '''
    密码格式检验
    :param password:
    :return:
    '''

    if len(password) < 8 :
        return False, gettext('Password at least 8 characters! And at least contain Numbers, letters, special characters of two kinds')
    else:
        too_simple = True
        last_ac = False
        for p in password:
            _ac = ord(p)
            if last_ac:
                if _ac != last_ac+1:
                    too_simple = False
                    break
            last_ac = _ac
        if too_simple:
            return False,gettext('The password is too simple, can not use continuous characters!')
    return True,""