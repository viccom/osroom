# -*-coding:utf-8-*-
from flask import request, session
from flask_babel import gettext

from apps.app import rest_session
from apps.core.utils.get_config import get_config

__author__ = "Allen Woo"

def language_set():

    lan = request.argget.all('language', "zh_CN")
    session["language"] = lan
    if request.headers.get('OSR-ClientId'):
        rest_session.set("language", lan)
    else:
        session["language"] = lan

    if lan in list(get_config('babel', 'LANGUAGES').keys()):
        data = {"msg_type":"s", "msg":gettext("Set up language success"), "http_status":201}
    else:
        data = {"msg_type": "e", "msg": gettext("Does not support this language"),
                "http_status": 400}

    return data