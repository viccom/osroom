#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = "Allen Woo"

def get_num_digits(num):
    n = 0
    while True:
        if not num:
            break
        n += 1
        num = int(num) >> 1
    return n