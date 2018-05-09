# -*-coding:utf-8-*-
from apps.core.flask.login_manager import osr_login_required
from apps.core.blueprint import api
from apps.core.flask.response import response_format
from apps.modules.verification_code.process.image_code import get_code
from apps.modules.verification_code.process.send_code import send_code

__author__ = 'Allen Woo'
@api.route('/vercode/send', methods=['POST'])
def api_send_code():

    '''
    POST:
        手机或邮箱验证码发送
        account_type:<str>, "email" or "mobile_phone"
        account:<email or number>, 接收验证码的账户
        exist_account:<int>, 是否只能发送给用该邮箱/号码在本平台已注册的用户? 1为是, 0为否. 默认0

        如果1分钟内,同一IP,同一用户(未登录的同属一匿名用户)
        调用api超过MAX_NUM_SEND_SAMEIP_PERMIN_NO_IMGCODE(1分钟内无图片验证码最大调用次数)配置的次数,
        超过后API会生会返回open_img_verif_code:true,
        表示需要图片验证码验证,客户端应该请求验证码/api/vercode/image,
        再次提交登录时需要以下两个参数
        code:<str>, 图片验证码中的字符
        code_url_obj:<json>, 图片验证码url 对象

        注意:如果你并不想使用图片验证码来防止频繁调用,请在管理的设置MAX_NUM_SEND_SAMEIP_PERMIN_NO_IMGCODE的值大于
        MAX_NUM_SEND_SAMEIP_PERMIN
        :return:
    '''

    data = send_code()
    return response_format(data)


@api.route('/vercode/image', methods=['GET'])
def api_get_image_code():

    '''
    GET:
        获取图片验证码
        :return: 验证码path object
    '''

    data = get_code()
    return response_format(data)
