# -*-coding:utf-8-*-
import platform

import os
from PIL import Image
from apps.configs.sys_config import STATIC_PATH, VERSION

__author__ = 'Allen Woo'

def start_info():
    '''
    启动时, 打印系统信息
    :return:
    '''

    width = 77
    height = 7
    logo_path = "{}/admin/sys_imgs/osroom-logo.png".format(STATIC_PATH)
    if os.path.exists(logo_path):
        im = Image.open(logo_path)
        im = im.resize((width, height), Image.NEAREST)
        txt = ""
        for i in range(height):
            for j in range(width):
                ch = get_char(*im.getpixel((j, i)))
                if ch == "*":
                    ch = "\033[1;35m{}\033[0m".format(ch)
                else:
                    ch = "\033[1;36m{}\033[0m".format(ch)
                txt += ch
            txt += '\n'
        print(txt)

    version = VERSION
    info = '''
    Welcome to use the osroom open source web system.
    osroom v{}
    osroom website: \033[1;34m http://osroom.com \033[0m
    Project code download: \033[1;34m https://github.com/osroom/osroom \033[0m
    License: BSD2
    The operating system: {}
    Server started...
    '''.format(version, platform.system())
    print(info)

def get_char(r, b, g, alpha=256):

    ascii_char = list("*. ")
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (512.0 + 1) / length
    return ascii_char[int(gray / unit)]