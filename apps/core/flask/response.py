# -*-coding:utf-8-*-
from flask import Response, jsonify

__author__ = 'Allen Woo'

class OsrResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(OsrResponse, cls).force_type(rv, environ)


def response_format(data, status=200):

    '''
    :param data:
    :param status:http status
    :return:
    '''

    if not isinstance(data, dict):
        return data, status
    if "http_status" not in data.keys():
        return data, status
    return data, data["http_status"]