# -*-coding:utf-8-*-
from flask import request
from flask_babel import gettext
from apps.app import mdb_user
from apps.core.flask.reqparse import arg_verify
from apps.modules.message.process.user_message import insert_user_msg
from apps.utils.send_msg.send_email import send_email
from apps.utils.format.obj_format import json_to_pyseq
from apps.utils.send_msg.send_message import send_mobile_msg

__author__ = "Allen Woo"

def send_msg():

    '''
    发送消息
    :return:
    '''

    title = request.argget.all("title")
    content = request.argget.all("content")
    content_html = request.argget.all("content_html")
    send_type = json_to_pyseq(request.argget.all("send_type",[]))
    username = json_to_pyseq(request.argget.all("username", []))

    s, r = arg_verify([(gettext(gettext("title")), title),
                       (gettext("content"), content_html),
                       (gettext("send type"), send_type),
                       (gettext("user name"), username)],
                      required=True)
    if not s:
        return r

    data = {"msg":"", "msg_type":"s"}
    query = {"is_delete": {"$in": [False, 0, ""]}, "active": {"$in": [True, 1]}}
    if len(username) > 1 or username[0].lower() != "all":
        # 不是发给全部用户
        query["username"] = {"$in": username}

    users = list(mdb_user.db.user.find(query, {"_id": 1, "email": 1, "mphone_num":1}))

    for send_t in send_type:
        if send_t == "on_site":
            for user in users:
                insert_user_msg(user_id=user["_id"], ctype="notice", label="sys_notice",
                                title=title, content={"text":content}, is_sys_msg=True)

            if users:
                data["msg"] = "{}. {}".format(data["msg"], gettext("Station news success"))
            else:
                data["msg"] = "{}. {}".format(data["msg"], gettext("No relevant user"))
                data["msg_type"] = "w"

        elif send_t == "email":

            to_emails = []
            for user in users:
                to_emails.append(user["email"])

            if to_emails:
                send_email(subject=title,
                           recipients=to_emails,
                           html_msg=content_html)
                data["msg"] = "{}. {}".format(data["msg"], gettext("Mail message is being sent"))
            else:
                data["msg"] = "{}. {}".format(data["msg"], gettext("There is no such email address user"))
                data["msg_type"] = "w"

        elif send_t == "sms":
            # 发送短信
            to_mnumber = []
            for user in users:
                if "mphone_num" in user:
                    to_mnumber.append(user["mphone_num"])

            if to_mnumber:
                send_mobile_msg(to_mnumber, content)

                data["msg"] = "{}. {}".format(data["msg"], gettext("SMS sent"))
            else:
                data["msg"] = "{}. {}".format(data["msg"], gettext("No user mobile phone number was obtained"))
                data["msg_type"] = "w"

    data["msg"]= data["msg"].strip(". ")
    data["http_status"] = 201
    return data

