# -*-coding:utf-8-*-
import getopt
import sys
from apps.configs.sys_config import PROJECT_PATH

__author__ = "Allen Woo"

def main():
    '''
    脚本主函数
    :return:
    '''
    from tools.usage import usage_help
    s_ops = "h"
    s_opexplain = ["help"]
    l_ops = ["up-pylib=", "up-conf-sample", "add-user"]
    l_opexplain = [
                   "<value>, Check the python package needed to update the system.\n\t\t"
                   "Optional parameters: 'input-venv' or 'no-input-venv'",

                   "Update the system configuration sample file. Automatically remove sensitive data (eg passwords)\n\t\t"
                   "Mainly the following configuration files:\n\t\t"
                   "{}/apps/config_sample.py; {}/apps/db_config_sample.py".format(PROJECT_PATH, PROJECT_PATH),

                   "Add a Root user, generally only used to initialize the user when the site was just created"
                ]

    action = ["Update python lib: python {} --up-pylib no-input-venv".format(__file__),
              "Update config sample: python {} --up-conf-sample".format(__file__),
              "Add user: python {} --add-user".format(__file__)
              ]

    opts, args = getopt.getopt(sys.argv[1:],s_ops , l_ops)
    for op, value in opts:
        if op == "--up-pylib":
            from apps.core.utils.sys_tool import update_pylib
            if value == "input-venv":
                update_pylib()
            else:
                update_pylib(input_venv_path=False)

        elif op == "--up-conf-sample":
            from apps.core.utils.sys_tool import copy_config_to_sample
            copy_config_to_sample()

        elif op == "--add-user":
            from start import mdb_user
            from apps.core.utils.sys_tool import add_user
            add_user(mdb_user)

        elif op == "-h" or op == "--help":

            usage_help(s_ops, s_opexplain, l_ops, l_opexplain, action=action)
    if not opts:

        usage_help(s_ops, s_opexplain, l_ops, l_opexplain, action=action)

if __name__ == '__main__':
    main()
