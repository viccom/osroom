# -*-coding:utf-8-*-
from apps.utils.verify.img_verify_code import create_img_code

__author__ = "Allen Woo"

def get_code():

    '''
    获取图片验证码
    :return:
    '''
    data = {"msg_type":"s", "http_status":200}
    code = create_img_code()
    data['code'] = code
    return data