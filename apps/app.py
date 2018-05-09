# -*-coding:utf-8-*-
__author__ = 'Allen Woo'
from apps.core.flask.myflask import OsrApp
from apps.core.flask.cache import Cache
from apps.core.flask.rest_session import RestSession
from apps.core.db.mongodb import PyMongo
from apps.core.logger.web_logging import WebLogger, web_start_log
from flask_babel import Babel
from flask_mail import Mail
from flask_oauthlib.client import OAuth
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from redis import StrictRedis
from apps.configs.db_config import DB_CONFIG


'''
 Flask app 与其他核心模块实例化
 注意: 不要将模块初始话设置放在本文件
'''
# 主程序
web_start_log.info("Initialize the OsrApp")
app = OsrApp(__name__)
web_start_log.info("Instance of each module")
mdb_web = PyMongo()
mdb_sys = PyMongo()
mdb_user = PyMongo()
cache = Cache()
babel = Babel()
csrf = CSRFProtect()
login_manager = LoginManager()
sess = Session()
rest_session = RestSession()
mail = Mail()
weblog = WebLogger()
oauth = OAuth()
redis = StrictRedis(host=DB_CONFIG["redis"]["host"][0],
                    port=DB_CONFIG["redis"]["port"][0],
                    password=DB_CONFIG["redis"]["password"])

