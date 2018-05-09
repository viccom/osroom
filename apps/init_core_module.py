# -*-coding:utf-8-*-
from apps.core.db.config_mdb import DatabaseConfig
from apps.core.logger.web_logging import web_start_log
from apps.configs.config import CONFIG
from apps.utils.format.obj_format import ConfDictToClass
from apps.app import login_manager, redis, sess, cache, csrf, babel, mdb_web, \
    mdb_sys, mdb_user, mail, oauth, weblog, rest_session
from apps.configs.sys_config import CONFIG_CACHE_KEY, BABEL_TRANSLATION_DIRECTORIES, SESSION_PROTECTION, \
    SESSION_COOKIE_PATH, SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SECURE, CSRF_ENABLED, WTF_CSRF_CHECK_DEFAULT, \
    WTF_CSRF_METHODS, SESSION_USE_SIGNER, PRESERVE_CONTEXT_ON_EXCEPTION, PLUG_IN_CONFIG_CACHE_KEY

'''
初始化一些核心模块
'''

def init_core_module(app):

    '''
    初始化核心模块
    :param app:
    :return:
    '''
    # app config
    web_start_log.info("Initialize the core module")

    # 系统必要配置, 优先导入
    app.config.from_object(ConfDictToClass(CONFIG["system"], key="value"))
    app.config.from_object(ConfDictToClass(CONFIG["key"], key="value"))

    # 数据库
    app.config.from_object(DatabaseConfig())
    mdb_web.init_app(app, config_prefix='MONGO_WEB')
    mdb_sys.init_app(app, config_prefix='MONGO_SYS')
    mdb_user.init_app(app, config_prefix='MONGO_USER')

    # 缓存
    app.config.from_object(ConfDictToClass(CONFIG["cache"], key="value"))
    app.config["CACHE_REDIS"] = redis
    app.config["CACHE_MONGODB"] = mdb_sys.connection
    app.config["CACHE_MONGODB_DB"] = mdb_sys.name
    cache.init_app(app)

    # 清除配置CONFIG的cache
    with app.app_context():
        msg = " * Clean configuration cache successfully"
        cache.delete(CONFIG_CACHE_KEY)
        cache.delete(PLUG_IN_CONFIG_CACHE_KEY)
        web_start_log.info(msg)
        print(msg)

    # 异常错误信息
    app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = PRESERVE_CONTEXT_ON_EXCEPTION

    ###################################################
    # 在此之前, 任何程序不能调用utils.get_config.py下的方法
    ###################################################

    from apps.core.utils.get_config import get_configs
    from apps.core.flask.request import OsrRequestProcess
    from apps.core.flask.errorhandler import ErrorHandler
    from apps.core.blueprint import api, admin_view, theme_view, static, open_api
    from apps.core.flask.routing import RegexConverter
    from apps.core.flask.routing import push_url_to_db

    # Session会话配置
    session_config = get_configs("session")
    session_config["SESSION_PROTECTION"] = SESSION_PROTECTION
    session_config["SESSION_COOKIE_PATH"] = SESSION_COOKIE_PATH
    session_config["SESSION_COOKIE_HTTPONLY"] = SESSION_COOKIE_HTTPONLY
    session_config["SESSION_COOKIE_SECURE"] = SESSION_COOKIE_SECURE
    session_config["SESSION_USE_SIGNER"] = SESSION_USE_SIGNER
    session_config["SESSION_MONGODB_DB"] = mdb_sys.name

    app.config.from_object(ConfDictToClass(session_config))
    app.config["SESSION_REDIS"] = redis
    app.config["SESSION_MONGODB"] = mdb_sys.connection
    sess.init_app(app)
    rest_session.init_app(app)

    # 邮件
    app.config.from_object(ConfDictToClass(get_configs("email")))
    mail.init_app(app)

    # Csrf token
    csrf_config = {}
    csrf_config["CSRF_ENABLED"] = CSRF_ENABLED
    csrf_config["WTF_CSRF_CHECK_DEFAULT"] = WTF_CSRF_CHECK_DEFAULT
    csrf_config["WTF_CSRF_METHODS"] = WTF_CSRF_METHODS
    app.config.from_object(ConfDictToClass(csrf_config))
    csrf.init_app(app)

    # Babel
    app.config.from_object(ConfDictToClass(get_configs("babel")))
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = BABEL_TRANSLATION_DIRECTORIES
    babel.init_app(app)

    # 登录管理
    login_manager.init_app(app)
    #login_manager.anonymous_user = AnonymousUser()
    login_manager.session_protection = SESSION_PROTECTION

    weblog.init_app(app)
    oauth.init_app(app)
    # 让路由支持正则
    app.url_map.converters['regex'] = RegexConverter

    # 注册蓝图 blueprint
    web_start_log.info("Register blueprint, Initialize the routing")
    app.register_blueprint(api)
    app.register_blueprint(open_api)
    app.register_blueprint(admin_view)
    app.register_blueprint(theme_view)
    app.register_blueprint(static)
    push_url_to_db(app)

    # 请求处理
    request_process = OsrRequestProcess()
    request_process.init_request_process(app=app)
    request_process.init_babel_locale_selector(babel=babel)

    # 错误处理
    ErrorHandler(app)