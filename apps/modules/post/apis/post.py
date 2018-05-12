# -*-coding:utf-8-*-
from flask import request
from apps.core.flask.login_manager import osr_login_required
from apps.configs.sys_config import METHOD_WARNING
from apps.core.blueprint import api
from apps.core.flask.response import response_format
from apps.modules.post.process.post import get_post, get_posts, post_like

__author__ = 'Allen Woo'
@api.route('/post', methods=['GET'])
def api_post():

    '''
    GET:
        1.获取一篇文章
        post_id:<str>,post id

        2.根据条件获取文章
        sort:<array>,排序, 1表示升序, -1表示降序.如:
            按时间降序 [{"issue_time":-1},{"update_time":-1}]
            按时间升序 [{"issue_time": 1},{"update_time": 1}]
            先后按赞(like)数降序, 评论数降序,pv降序, 发布时间降序
            [{"like": -1}, {"comment_num": -1}, {"pv": -1},{"issue_time": -1}]
            默认时按时间降序, 也可以用其他字段排序
        status:<int> , "is_issued"（正常发布） or "draft"（草稿） or "not_audit"（等待审核） or "unqualified"（未通过审核） or "recycle"(用户的回收站) or "user_remove"
            （user_remove是指用户永久删除或被管理删除的）

        matching_rec:<str>,可选，提供一段内容, 匹配一些文章推荐
        time_range:<int>,可选,单位为天,比如最近7天的文章
        page:<int>,第几页，默认第1页
        pre:<int>, 每页查询多少条
        keyword:<str>, Search keywords, 搜索使用
        fields:<array>, 需要返回的文章字段,如["title"]
        unwanted_fields:<array>, 不能和fields参数同时使用,不需要返回的文章字段,如["user_id"]
        user_id:<str>, 如需获取指定用户的post时需要此参数
        category_id:<str>, 获取指定文集的post时需要此参数

    '''

    if request.c_method == "GET":
        if request.argget.all('post_id'):
            data = get_post()
        else:
            data = get_posts()
    else:
        data = {"msg_type":"w", "msg":METHOD_WARNING, "http_status":405}
    return response_format(data)


@api.route('/post', methods=['PUT'])
@osr_login_required
def api_post_op():

    '''
    PUT:
        喜欢文章
        action:<str>, 可以是like(点赞文章)
        id:<str>, post id

    '''
    if request.c_method == "PUT":
        if request.argget.all('action') == "like":
            data = post_like()
    else:
        data = {"msg_type":"w", "msg":METHOD_WARNING, "http_status":405}
    return response_format(data)