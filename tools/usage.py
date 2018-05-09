#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = "Allen Woo"

import sys

__author__ = 'Allen Woo'

def usage_help(short_ops, short_opexplain, long_ops=[], long_opexplain=[], usage=[], action=[]):
    if usage:
        print("Usage:")
        for u in usage:
            print("\t{}".format(u))

    print("[option]:")
    s_op = short_ops.strip(":").split(":")
    i = 0
    for v in s_op:
        if len(v) != 1:
            v2_n = 0
            for v2 in v:
                print("\t-{}: {}".format(v2, short_opexplain[v2_n+i]))
                v2_n += 1
            i += len(v)
        else:
            print("\t-{}: {}".format(v, short_opexplain[i]))
            i += 1
    # long
    l = len(long_ops)
    for i in range(0, l):
        print("\t--{}: {}".format(long_ops[i].strip("="), long_opexplain[i]))

    if action:
        print("[action]:")
        for a in action:
            print("\t{}".format(a))
    print("\n")
    sys.exit()
