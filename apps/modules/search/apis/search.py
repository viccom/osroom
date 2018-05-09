# -*-coding:utf-8-*-
from apps.core.blueprint import api
from apps.core.flask.response import response_format
from apps.modules.search.process.search import search_process

__author__ = "Allen Woo"


@api.route('/search', methods=['GET'])
def api_search():

    '''
    GET:
        搜索(暂不支持全文搜索), 只能搜索文章, 用户
        keyword:<str>, Search keywords
        target:<str>, 可选"post" 或 "user". 不使用此参数则搜索所有可选目标
        page:<int>,第几页，默认第1页
        pre:<int>, 每页多少条

    '''

    data = search_process()
    return response_format(data)