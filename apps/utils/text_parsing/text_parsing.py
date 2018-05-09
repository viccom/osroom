# -*-coding:utf-8-*-
from lxml import etree

__author__ = "Allen Woo"

def richtext_extract_img(richtext=""):

    # 获取富文本中使用的图片
    s = etree.HTML(richtext.lower())
    srcs = s.xpath("//img/@src")
    return srcs