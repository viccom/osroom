#-*-coding:utf-8-*-
import sys
from signal import signal, SIGCHLD, SIG_IGN
from apps.configs.config import CONFIG
from apps.core.db.config_mdb import DatabaseConfig
from apps.core.utils.sys_tool import update_pylib, add_user as add_user_process

__author__ = 'all.woo'

'''
manage
'''
# 更新python第三方库
print(" * Check or update Python third-party libraries")
CONFIG["py_venv"]["VENV_PATH"]["value"] = sys.prefix
update_pylib(input_venv_path = False)

# 网站还未启动的时候, 连接数据库, 更新collection
from apps.core.utils.update_db_collection import update_mdb_collections
from apps.core.db.mongodb import PyMongo
print(" * Check or update the database collection")
database = DatabaseConfig()
mdb_web = PyMongo()
mdb_sys = PyMongo()
mdb_user = PyMongo()
db_init = 2
while db_init:
    mdb_web.init_app(config_prefix='MONGO_WEB', db_config=database.MONGO_WEB_URI)
    mdb_sys.init_app(config_prefix='MONGO_SYS', db_config=database.MONGO_SYS_URI)
    mdb_user.init_app(config_prefix='MONGO_USER', db_config=database.MONGO_USER_URI)
    if db_init == 2:
        update_mdb_collections(mdb_user=mdb_user, mdb_web=mdb_web, mdb_sys=mdb_sys)
    db_init -= 1

# 更新配置文件
from apps.core.flask.update_config_file import update_config_file
print(" * Update and sync config.py")
r = update_config_file(mdb_sys=mdb_sys)
if not r:
    print("[Error] Update profile error, check log sys_start.log")
    sys.exit(-1)
del CONFIG["py_venv"]


# 启动网站
from flask_script import Manager
from apps.app import app
from apps.core.flask.module_import import module_import
from apps.init_core_module import init_core_module
from apps.configs.sys_config import MODULES
from apps.sys_startup_info import start_info

start_info()
init_core_module(app)
module_import(MODULES)
manager = Manager(app)
if not "--debug" in sys.argv and not "-D" in sys.argv:
    print(" * Signal:(SIGCHLD, SIG_IGN).Prevent child processes from becoming [Defunct processes].(Do not need to comment out)")
    signal(SIGCHLD, SIG_IGN)

@manager.command
def add_user():
    add_user_process(mdb_user)

if __name__ == '__main__':
    manager.run()