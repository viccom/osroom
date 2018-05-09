# -*-coding:utf-8-*-
from importlib import import_module
__author__ = "Allen Woo"

def module_import(modules):

    for module in modules:
        import_module(module)