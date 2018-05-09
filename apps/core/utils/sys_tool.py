# -*-coding:utf-8-*-
import json
import os
import re
import sys
import subprocess
from getpass import getpass
from copy import deepcopy
from apps.configs.config import CONFIG
from apps.configs.sys_config import PROJECT_PATH
from apps.core.logger.web_logging import web_start_log

__author__ = "Allen Woo"

def copy_config_to_sample():

    '''
    复制config.py到config_sample,　并把密码替换掉，以免暴露到网上
    复制db_account.py到db_account_sample,　并把密码替换掉，以免暴露到网上
    '''

    from apps.configs.config import __readme__
    from apps.configs.db_config import DB_CONFIG

    local_config = deepcopy(CONFIG)
    for k,v in local_config.items():
        for k1,v1 in v.items():
            if k1.startswith("__") and k1.endswith("__"):
                continue
            if "type" in v1 and v1["type"] == "password":
                v1["value"] = "<Your password>"
            elif not "type" in v1:
                print("[ERROR] Check that the configuration of {}>{} is correct".format(k,k1))
                sys.exit(-1)

    # 复制配置文件为sample配置文件
    info = '''# -*-coding:utf-8-*-\n__author__ = "Allen Woo"\n'''
    doc = "__readme__='''{}'''\n".format(__readme__)

    temp_conf = str(json.dumps(local_config, indent=4, ensure_ascii=False))
    wf = open("{}/apps/configs/config_sample.py".format(PROJECT_PATH), "wb")

    wf.write(bytes(info, "utf-8"))
    wf.write(bytes(doc, "utf-8"))
    wf.write(bytes("# Danger: If True, the database configuration data will be overwritten\n", "utf-8"))
    wf.write(bytes("# 危险:如果为True, 则会把该文件配置覆盖掉数据库中保存的配置\n", "utf-8"))
    wf.write(bytes("OVERWRITE_DB = False\n", "utf-8"))
    wf.write(bytes("CONFIG = ", "utf-8"))
    wf.write(bytes(temp_conf.replace("false", "False").replace("true", "True").replace("null", "None"), "utf-8"))
    wf.close()
    print("It has been updated config_sample.py")


    # 复制db_config.py 到　db_config_sample.py
    local_config = deepcopy(DB_CONFIG)
    for k, v in local_config.items():
        if isinstance(v, dict):
            for k1, v1 in v.items():
                if k1 == "password":
                    v[k1] = "<Your password>"
                elif isinstance(v1, dict):
                    for k2,v2 in v1.items():
                        if k2 == "password":
                            v1[k2] = "<Your password>"


    # 复制配置文件为sample配置文件
    info = '''# -*-coding:utf-8-*-\n__author__ = "Allen Woo"\n'''
    temp_conf = str(json.dumps(local_config, indent=4, ensure_ascii=False))
    wf = open("{}/apps/configs/db_config_sample.py".format(PROJECT_PATH), "wb")
    wf.write(bytes(info, "utf-8"))
    wf.write(bytes("DB_CONFIG = ", "utf-8"))
    wf.write(bytes(temp_conf.replace("false", "False").replace("true", "True").replace("null", "None"), "utf-8"))
    wf.close()
    print("It has been updated db_config_sample.py")


def add_user(mdb_user):

    '''
    初始化root用户角色, 管理员, 管理员基本资料

    :return:
    '''
    from werkzeug.security import generate_password_hash
    from apps.utils.validation.str_format import ver_name, email_format_ver, password_format_ver
    from apps.modules.user.models.user import user_model

    print(' * [User] add')
    is_continue = False
    while True:
        username = input("Input username:")
        if re.search(r"[\.\*#\?]+", username):
            print("[Warning]: The name format is not correct,You can't use '.','*','#','?'\n")
        else:
            break

    while not is_continue:
        email = input("Input email:")
        s,r = email_format_ver(email)
        if not s:
            print("[Warning]: {}".format(r))
        else:
            break

    while not is_continue:
        password = getpass("Input password(Password at least 8 characters):")
        s,r = password_format_ver(password)
        if not s:
            print("[Warning]: {}\n".format(r))
        else:
            break
    try:
        mdb_user.db.create_collection("role")
        print(' * Created role collection')
    except:
        pass
    try:
        mdb_user.db.create_collection("user")
        print(' * Created user collection')
    except:
        pass

    root_per = 0b11111111111111111111111111111111
    role_root = mdb_user.db.role.find_one({"permissions":root_per})
    if not role_root:
        print(" * Create root role...")
        r = mdb_user.db.role.insert_one({"name":"Root",
                                        "default":0,
                                        "permissions":root_per,
                                        "instructions":'ROOT'})

        if r.inserted_id:
            print("Create root user role successfully")
        else:
            print("[Error] Failed to create superuser role")
            sys.exit(-1)

        root_id = r.inserted_id
    else:
        root_id = role_root['_id']

    password_hash = generate_password_hash(password)
    user = mdb_user.db.user.find_one({"$or":[{"username":username}, {"email":email}]})
    if user:
        mdb_user.db.user.update_one({"_id":user["_id"]},
                                {
                                    "$set":{"password":password_hash, "role_id":root_id}
                                 })
        print(" * This user already exists, updated password.")
    else:
        print(' * Create root user...')
        user = user_model(username=username, email=email, password=password, custom_domain=-1, role_id=root_id, active=True)
        r = mdb_user.db.user.insert_one(user)
        if r.inserted_id:
            print(" * Create a root user role successfully")
        else:
            print(" * [Error] Failed to create a root user role")
            sys.exit(-1)

    # To create the average user role
    average_user = mdb_user.db.role.find_one({"permissions":CONFIG["permission"]["USER"]["value"]})
    if not average_user:
        print(" * Create the average user role...")
        r = mdb_user.db.role.insert_one({
            "name":"User",
            "default":1,
            "permissions":CONFIG["permission"]["USER"]["value"],
            "instructions":'The average user',
        })
        if r.inserted_id:
            print(" * Create a generic user role successfully")
        else:
            print(" * Failed to create a generic user role")

    role = mdb_user.db.role.find_one({"_id":root_id})
    hidden_password = "{}****{}".format(password[0:2], password[6:])
    print('The basic information is as follows')
    print('Username: {}\nEmail: {}\nUser role: {}\nPassword: {}'.format(username, email, role["name"], hidden_password))
    print('End')

def update_pylib(input_venv_path = True):

    '''
    更新python环境库
    :param need_input:
    :return:
    '''
    if input_venv_path:
        try:
            input_str = input("Already running this script in your project python virtual environment?(yes/no):\n")
            if input_str.upper() == "YES":
                venv_path = None
            else:
                venv_path =  CONFIG["py_venv"]["VENV_PATH"]["value"]
                input_str = input("The default path is: {}, Use the default(yes/no)\n".format(venv_path))
                if input_str.upper() != "YES":
                    venv_path = input("Enter a virtual environment:\n")
        except:
            venv_path = CONFIG["py_venv"]["VENV_PATH"]["value"]
    else:
        venv_path = CONFIG["py_venv"]["VENV_PATH"]["value"]

    if venv_path:
        if os.path.exists("{}/bin/activate".format(venv_path)):
            venv = ". {}/bin/activate && ".format(venv_path)
        else:
            venv = ". {}/bin/activate && ".format(sys.prefix)
    else:
        venv = ""

    print(" * Update pip...")
    s, r = subprocess.getstatusoutput("{}pip3 install -U pip".format(venv))
    print(r)

    s,r = subprocess.getstatusoutput("{}pip3 freeze".format(venv))
    old_reqs = r.split()
    with open("{}/requirements.txt".format(PROJECT_PATH)) as rf:
        new_reqs = rf.read().split()

    # 查找需要安装的包
    ret_list = list(set(new_reqs)^set(old_reqs))
    install_list = []
    for ret in ret_list:
        if (not ret in old_reqs) and (ret in new_reqs):
            install_list.append(ret)

    if install_list:
        msg = " * To install the following libs"
        print(msg)
        print(install_list)
        if not input_venv_path:
            web_start_log.info(msg)
            web_start_log.info(install_list)
            pass

    install_failed = []
    for sf in install_list:
        print(venv, sf)
        s, r = subprocess.getstatusoutput("{}pip3 install -U {}".format(venv, sf))
        if s:
            install_failed.append(sf)

    for sf in install_failed:
        s, r = subprocess.getstatusoutput("{}pip3 install -U {}".format(venv, sf))
        if not s:
            install_failed.remove(sf)
    if install_failed:
        msg = " * Installation failed library, please manually install"
        print(msg)
        print(install_failed)
        web_start_log.info(msg)
        web_start_log.info(install_failed)

    # 查找需要卸载的包
    s,r = subprocess.getstatusoutput("{}pip3 freeze".format(venv))
    old_reqs = r.split()
    ret_list = list(set(new_reqs)^set(old_reqs))
    uninstall_list = []
    for ret in ret_list:
        if (ret in old_reqs) and (not ret in new_reqs):
            uninstall_list.append(ret)

    for sf in uninstall_list[:]:
        if not "==" in sf:
            uninstall_list.remove(sf)

    if uninstall_list:
        msg = " * Now don't need python library:"
        print(msg)
        print(uninstall_list)
        if not input_venv_path:
            web_start_log.info(msg)
            web_start_log.info(uninstall_list)
