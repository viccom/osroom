#!/usr/bin/env python
# -*-coding:utf-8-*-
import json
import sys
import regex as re
from pymongo.cursor import Cursor

__author__ = "Allen Woo"
def objid_to_str(datas, fields=["_id"]):
    '''
    mongodb ObjectId to str
    :param datas:
    :param field:
    :return:
    '''
    if isinstance(datas, (list, Cursor)):
        _datas = []
        for data in datas:
            for field in fields:
                data[field] = str(data[field])
            _datas.append(data)
        return _datas
    else:
        datas_keys = datas.keys()
        for field in fields:
            if field in datas_keys:
                datas[field] = str(datas[field])

        return datas

def json_to_pyseq(tjson):
    '''
    json to python sequencer
    :param json:
    :return:
    '''
    if tjson in [None, "None"]:
        return None
    elif not isinstance(tjson, (list, dict, tuple)) and tjson != "":

        if isinstance(tjson, (str, bytes)) and tjson[0] not in ["{", "["]:
            return tjson
        try:
            tjson = json.loads(tjson)
        except:
            tjson = eval(tjson)
        else:
            if isinstance(tjson, str):
                tjson = eval(tjson)
    return tjson

def str_to_num(string, type=int):
    '''
    字符串转数字
    :param string: 字符串
    :param type: 转变方法(obj)
    :return:
    '''
    try:
        return type(string)
    except:
        if string:
            return 1
        elif not string or string.lower() == "false":
            return 0


class ConfDictToClass(object):
    def __init__(self,config, key=None):
        if not isinstance(config, dict):
            print("[ERROR]:Must be a dictionary")
            sys.exit(-1)
        if key == "value":
            for k,v in config.items():
                if not re.search(r"^__.*__$", k):
                    self.__dict__[k] = v["value"]
        else:
            for k,v in config.items():
                self.__dict__[k] = v

    # def __setattr__(self, name, value):
    #     if name == 'map':
    #          object.__setattr__(self, name, value)
    #          return;
    #     print('set attr called ',name,value)
    #     self.map[name] = value
    #
    # def __getattr__(self,name):
    #     v = self.map[name]
    #     if isinstance(v,(dict)):
    #         return v["value"]
    #     else:
    #         return self.map[name];
    #
    # def __getitem__(self,name):
    #     return self.map[name]