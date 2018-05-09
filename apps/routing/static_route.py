# -*-coding:utf-8-*-
import os
from flask import send_file, request
from werkzeug.exceptions import abort
from apps.app import csrf
from apps.configs.sys_config import ADMIN_STATIC_FOLDER
from apps.core.blueprint import static, theme_view
from apps.core.flask.permission import page_permission_required
from apps.core.utils.get_config import get_config
from apps.utils.format.obj_format import str_to_num

from apps.utils.image.image import ImageCompression

__author__ = "Allen Woo"

"""
 静态文件路由
 提示:
 1. static_size_img：　
    apps/static下图片路由: /static/<regex(".*\..+"):path>
    参数w,h可指定图片大小
 2. theme_static：
    themes主题static下静态文件路由：/<theme name>/static/<regex(".*"):path>
    参数w,h可指定图片大小
"""

#####################################################
# apps/static静态文件路由
#####################################################
@csrf.exempt
@static.route('/<regex(".+"):path>',methods=['GET'])
@page_permission_required()
def static_file(path):

    '''
    apps/static下静态文件获取(本视图函数只针对apps/static下的图片)，apps/static下其他可以直接哟你flask默认的

    注意：图片获取路由(apps/static下)
    参数w,h可指定图片大小
    :param path:原图片路径
    :param w:获取的宽
    :param h:获取的高
    :return:w和ｈ都大于0则返回相应尺寸图片; w和ｈ都等于0则返回原图; 其中一个值大于０则返回以这个值为基础等比缩放图片
    '''
    w = str_to_num(request.args.get("w", 0))
    h = str_to_num(request.args.get("h", 0))
    if w or h:
        path_list = os.path.splitext(path.rstrip().rstrip("/"))
        absolute_path = os.path.abspath("{}/{}_w_{}_h_{}{}".format(static.template_folder,
                                                                    path_list[0],
                                                                    w, h, path_list[1]))
        if not os.path.isfile(absolute_path):

            img_path = os.path.abspath("{}/{}".format(static.template_folder,path))
            try:
                imgcs = ImageCompression(img_path, absolute_path)
            except:
                abort(404)
            if w and h:
                # 自定义长宽
                imgcs.custom_pixels(w, h)
            else:
                # 等比缩放
                imgcs.isometric(w, h)

    else:
        absolute_path = os.path.abspath("{}/{}".format(static.template_folder, path))
        if not os.path.isfile(absolute_path):
            abort(404)
    return send_file(filename_or_fp=absolute_path,
                     conditional=True,
                     last_modified=True)


#####################################################
# apps/admin_pages/下静态文件路由
#####################################################

@csrf.exempt
@theme_view.route('/admin-pages/static/<regex(".+"):path>',methods=['GET'])
@page_permission_required()
def admin_static_file(path):

    '''
    获取admin_pages下静态文件
    :param path:文件路径
    '''
    absolute_path = os.path.abspath("{}/{}".format(ADMIN_STATIC_FOLDER, path))
    if not os.path.isfile(absolute_path):
        abort(404)
    return send_file(filename_or_fp=absolute_path,
                     conditional=True,
                     last_modified=True)

#####################################################
# apps/themes/下主题静态文件路由
#####################################################

@csrf.exempt
@theme_view.route('/theme/static/<regex(".+"):path>',methods=['GET'])
@page_permission_required()
def theme_static_file(path):

    '''
    获取主题下静态文件
    注意:
        theme主题图片获取路由 (目录themes/<theme name>/static下图片)
        1.对于图片,本路由只能获取目录themes/<theme name>/static下定义尺寸图片
        参数w,h可指定图片大小
    :param path:原图片路径
    :param w:获取的宽
    :param h:获取的高
    :return:w和ｈ都大于0则返回相应尺寸图片; w和ｈ都等于0则返回原图; 其中一个值大于０则返回以这个值为基础等比缩放图片
    '''
    w = str_to_num(request.args.get("w", 0))
    h = str_to_num(request.args.get("h", 0))
    if w or h:
        path_list = os.path.splitext(path.rstrip().rstrip("/"))

        absolute_path = os.path.abspath("{}/{}/static/{}_w_{}_h_{}{}".format(theme_view.template_folder,
                                                                   get_config("theme", "CURRENT_THEME_NAME"),
                                                                    path_list[0],
                                                                    w, h, path_list[1]))
        if not os.path.isfile(absolute_path):
            img_path = os.path.abspath("{}/{}/static/{}".format(theme_view.template_folder,
                                                                 get_config("theme", "CURRENT_THEME_NAME"),
                                                                 path))
            try:
                imgcs = ImageCompression(img_path, absolute_path)
            except:
                abort(404)
            if w and h:
                # 自定义长宽
                imgcs.custom_pixels(w, h)
            else:
                # 等比缩放
                imgcs.isometric(w, h)
    else:
        absolute_path = os.path.abspath("{}/{}/static/{}".format(theme_view.template_folder,
                                                                 get_config("theme", "CURRENT_THEME_NAME"),
                                                                 path))
        if not os.path.isfile(absolute_path):
            abort(404)
    return send_file(filename_or_fp=absolute_path,
                     conditional=True,
                     last_modified=True)