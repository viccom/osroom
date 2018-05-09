# -*-coding:utf-8-*-
from flask import Flask
from apps.core.flask.response import OsrResponse
__author__ = 'Allen Woo'

class OsrApp(Flask):
    response_class = OsrResponse