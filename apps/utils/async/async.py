#!/usr/bin/env python
#-*-coding:utf-8-*-
from multiprocessing import Process
import threading

__author__ = 'Allen Woo'
'''
decorators
'''

def async_thread(f):
    '''
    multiprocessing Process
    :param f:
    :return:
    '''
    def wrapper(*args, **kwargs):
        t =threading.Thread(target=f,args=args, kwargs = kwargs)
        t.start()
    return wrapper

def async_process(f):
    '''
    multiprocessing Process
    :param f:
    :return:
    '''
    def wrapper(*args, **kwargs):
        thr = Process(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper