# -*-coding:utf-8-*-
__author__ = "Allen Woo"
__readme__='''
################################################################################
1.本配置文件config_sample.py的内容全部复制(覆盖)到config.py
a.除了OVERWRITE_DB外, 其他配置都可以在平台管理端页面修改
b.启动网站/重启网站的时候，系统会自动合并数据库中保存的配置,实现本地配置文件配置与数据库一致.
c.如果你是开发人员,需要手动修改配置文件，请阅读下面说明

2.自动合并过程中:
a.对于本文件新增加的key会添加到数据库(value使用本地的)
b.本文文件没有的,而数据库有保存的key会在数据库删除
c.两边都存在的key, 则value使用数据库的

##如果你不想合并配置, 想用本地配置数据覆盖掉数据库中的配置数据,请修改变量OVERWRITE_DB

变量说明
*OVERWRITE_DB
启动系统时, 配置更新是否来自数据库, 以数据库中的value为主.
如果为True, 则完全以本文件数据上传到数据库中
如果为False, 按照上述[2.自动合并过程中],当次有效, 启动后会自动变为True

*CONFIG　
每个配置项中的__sort__作为在管理的显示的时候的排序使用
配置表,表中没有__info__的项目将不会出现在管理端的设置中
###############################################################################
'''
# Danger: If True, the database configuration data will be overwritten
# 危险:如果为True, 则会把该文件配置覆盖掉数据库中保存的配置
OVERWRITE_DB = False
CONFIG = {
    "upload": {
        "UP_ALLOWED_EXTENSIONS": {
            "type": "list",
            "info": "上传:允许上传的文件后缀(全部小写),每个用英文的','隔开",
            "value": [
                "xls",
                "xlxs",
                "excel",
                "txt",
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "gif",
                "ico",
                "mp4",
                "rmvb",
                "avi",
                "mkv",
                "mov",
                "mp3",
                "wav",
                "wma",
                "ogg",
                "zip",
                "gzip",
                "tar"
            ],
            "sort": 99
        },
        "IMG_VER_CODE_DIR": {
            "type": "string",
            "info": "系统生成的图片验证码保存目录",
            "value": "verifi_code",
            "sort": 99
        },
        "SAVE_DIR": {
            "type": "string",
            "info": "上传:保存目录,如何存在'/'则会自动切分创建子目录",
            "value": "media",
            "sort": 99
        },
        "__sort__": 99,
        "__restart__": "not_must",
        "__info__": "文件上传配置（建议技术管理人员使用）"
    },
    "comment": {
        "TRAVELER_COMMENT": {
            "type": "bool",
            "info": "游客评论开关,是否打开?",
            "value": False,
            "sort": 99
        },
        "MAX_LEN": {
            "type": "int",
            "info": "发布评论最多几个字符",
            "value": 300,
            "sort": 99
        },
        "NUM_PAGE_MAX": {
            "type": "int",
            "info": "每个页面最多获取几条评论(此配置对管理端无效)",
            "value": 30,
            "sort": 99
        },
        "OPEN_COMMENT": {
            "type": "bool",
            "info": "评论开关,是否打开评论功能?",
            "value": False,
            "sort": 99
        },
        "__sort__": 3,
        "INTERVAL": {
            "type": "int",
            "info": "控制评论频繁度时间(s)",
            "value": 30,
            "sort": 99
        },
        "NUM_OF_INTERVAL": {
            "type": "int",
            "info": "控制评论频繁度时间内最多评论几次",
            "value": 3,
            "sort": 99
        },
        "NUM_PAGE": {
            "type": "int",
            "info": "每个页面获取几条评论, 如果请求获取评论时指定了指定了per参数, 则此配置无效(此配置也对管理端无效)",
            "value": 10,
            "sort": 99
        },
        "__restart__": "not_must",
        "__info__": "评论内容设置"
    },
    "post": {
        "TAG_MAX_NUM": {
            "type": "int",
            "info": "POST标签最大个数",
            "value": 5,
            "sort": 99
        },
        "TITLE_MAX_LEN": {
            "type": "int",
            "info": "文章Title最大长度",
            "value": 50,
            "sort": 99
        },
        "BRIEF_LEN": {
            "type": "int",
            "info": "获取文章简要的字数",
            "value": 80,
            "sort": 99
        },
        "NUM_PAGE_MAX": {
            "type": "int",
            "info": "每个页面最多获取几篇文章(此配置对管理端无效)",
            "value": 30,
            "sort": 99
        },
        "__sort__": 2,
        "MAX_LEN": {
            "type": "int",
            "info": "发布文章最多几个字符",
            "value": 5000,
            "sort": 99
        },
        "NUM_PAGE": {
            "type": "int",
            "info": "每个页面获取几篇文章, 如果请求获取文章时指定了指定了per参数, 则此配置无效(此配置也对管理端无效)",
            "value": 10,
            "sort": 99
        },
        "TAG_MAX_LEN": {
            "type": "int",
            "info": "POST标签最多几个字",
            "value": 10,
            "sort": 99
        },
        "__restart__": "not_must",
        "__info__": "文章内容设置"
    },
    "key": {
        "SECRET_KEY": {
            "type": "string",
            "info": "安全验证码",
            "value": "ceavewrvwtrhdyjydj",
            "sort": 99
        },
        "__sort__": 99,
        "__info__": "安全Key（建议技术管理人员使用）",
        "SECURITY_PASSWORD_SALT": {
            "type": "string",
            "info": "安全密码码盐值",
            "value": "ceavewrvwtrhdyjydj",
            "sort": 99
        },
        "__restart__": "must"
    },
    "verify_code": {
        "MAX_IP_REQ_FREQ_PER_MIN": {
            "type": "int",
            "info": "同一IP地址,同一用户(未登录的同属同已匿名用户),每分钟允许调用API请求发送验证码最大次数,如果此配置<=MAX_IP_REQ_FREQ_MIN_NO_VERCODE,则MAX_IP_REQ_FREQ_MIN_NO_VERCODE自动失效",
            "value": 15,
            "sort": 99
        },
        "MIN_IMG_CODE_INTERFERENCE": {
            "type": "int",
            "info": "图片验证码干扰程度的最小值,最小值小于10时无效",
            "value": 10,
            "sort": 99
        },
        "SEND_CODE_TYPE": {
            "type": "dict",
            "info": "发送的验证码字符类型，与字符个数",
            "value": {
                "string": 0,
                "int": 6
            },
            "sort": 99
        },
        "__sort__": 99,
        "MAX_IP_REQ_FREQ_MIN_NO_VERCODE": {
            "type": "int",
            "info": "同一IP地址,同一用户(未登录的同属同已匿名用户),每分钟,允许在不验证[图片验证码]的时候,调用API请求发送验证码最大次数.超过后API会生成[图片验证码]并返回图片url对象.如果你的客户端(包括主题)不支持显示图片验证码,请设置此配置大于MAX_IP_REQ_FREQ_PER_MIN",
            "value": 99999,
            "sort": 99
        },
        "EXPIRATION": {
            "type": "int",
            "info": "验证码过期时间(s)",
            "value": 600,
            "sort": 99
        },
        "MAX_IMG_CODE_INTERFERENCE": {
            "type": "int",
            "info": "图片验证码干扰程度的最大值",
            "value": 40,
            "sort": 99
        },
        "__restart__": "not_must",
        "IMG_CODE_DIR": {
            "type": "string",
            "info": "图片验证码保存目录",
            "value": "admin/verify_code",
            "sort": 99
        },
        "__info__": "验证码(建议技术管理员配置)"
    },
    "category": {
        "__restart__": "not_must",
        "__sort__": 7,
        "__info__": "Web参数设置",
        "CATEGORY_TYPE": {
            "type": "dict",
            "info": "分类的品种只能有这几种",
            "value": {
                "音频库": "audio",
                "视频库": "video",
                "文本内容": "text",
                "文集": "post",
                "图库": "image",
                "其他": "other"
            },
            "sort": 99
        },
        "CATEGORY_MAX_LEN": {
            "type": "int",
            "info": "分类名称类型名最多几个字符",
            "value": 15,
            "sort": 99
        }
    },
    "session": {
        "SESSION_TYPE": {
            "type": "string",
            "info": "保存Session会话的类型,可选mongodb, redis",
            "value": "mongodb",
            "sort": 99
        },
        "SESSION_KEY_PREFIX": {
            "type": "string",
            "info": "添加一个前缀,之前所有的会话密钥。这使得它可以为不同的应用程序使用相同的后端存储服务器",
            "value": "osroom",
            "sort": 99
        },
        "__sort__": 99,
        "SESSION_PERMANENT": {
            "type": "bool",
            "info": "是否使用永久会话",
            "value": True,
            "sort": 99
        },
        "__restart__": "must",
        "SESSION_MONGODB_COLLECT": {
            "type": "string",
            "info": "Mongodb保存session的collection,当SESSION_TYPE为mongodb时有效",
            "value": "osr_session",
            "sort": 99
        },
        "__info__": "Session参数设置（建议技术管理人员使用）",
        "PERMANENT_SESSION_LIFETIME": {
            "type": "int",
            "info": "永久会话的有效期.",
            "value": 2592000,
            "sort": 99
        }
    },
    "cache": {
        "CACHE_TYPE": {
            "type": "string",
            "info": "缓存使用的类型,可选择redis,mongodb(<span style='color:red;'>注意:此参数,对程序中,使用cached时,指定了db_type的缓存无效</span>)",
            "value": "redis",
            "sort": 99
        },
        "USE_CACHE": {
            "type": "bool",
            "info": "是否使用缓存功能,建议开启(<span style='color:red;'>不开启会导致所有需要缓存的数据失去缓存功能</span>)",
            "value": True,
            "sort": 99
        },
        "CACHE_KEY_PREFIX": {
            "type": "string",
            "info": "所有键(key)之前添加的前缀,这使得它可以为不同的应用程序使用相同的memcached(内存)服务器.",
            "value": "osr_cache",
            "sort": 99
        },
        "__sort__": 99,
        "CACHE_MONGODB_COLLECT": {
            "type": "string",
            "info": "保存cache的collection(必须配置)",
            "value": "osr_cache",
            "sort": 99
        },
        "__restart__": "must",
        "CACHE_DEFAULT_TIMEOUT": {
            "type": "int",
            "info": "(s秒)默认缓存时间,当单个缓存没有设定缓存时间时会使用该时间",
            "value": 600,
            "sort": 99
        },
        "__info__": "Web缓存参数设置（建议技术管理人员使用）"
    },
    "name_audit": {
        "AUDIT_PROJECT_KEY": {
            "type": "dict",
            "info": "审核项目的Key(键),审核时会使用一个Key来获取审核规则,正则去匹配用户输入的内容",
            "value": {
                "username": "审核用户名",
                "class_name": "审核一些短的分类名称, 如category, tag"
            },
            "sort": 99
        },
        "__sort__": 8,
        "__info__": "名称验证, 如用户名,分类名称",
        "__restart__": "not_must"
    },
    "system": {
        "__restart__": "must",
        "TEMPLATES_AUTO_RELOAD": {
            "type": "bool",
            "info": "是否自动加载页面(html)模板.开启后,每次html页面修改都无需重启Web",
            "value": True,
            "sort": 99
        },
        "__info__": "其他web系统参数设置（建议技术管理人员使用）",
        "__sort__": 99
    },
    "rest_auth_token": {
        "LOGIN_LIFETIME": {
            "type": "int",
            "info": "jwt 登录BearerToken有效期(s)",
            "value": 2592000,
            "sort": 99
        },
        "MAX_SAME_TIME_LOGIN": {
            "type": "int",
            "info": "最多能同时登录几个使用JWT验证的客户端,超过此数目则会把旧的登录注销",
            "value": 3,
            "sort": 99
        },
        "REST_ACCESS_TOKEN_LIFETIME": {
            "type": "int",
            "info": "给客户端发的访问Token AccessToken的有效期",
            "value": 172800,
            "sort": 99
        },
        "__sort__": 99,
        "__restart__": "not_must",
        "__info__": "Web参数设置"
    },
    "site_config": {
        "MB_LOGO_DISPLAY": {
            "type": "string",
            "info": "移动端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则App name优先<br>可填<span style='color:red;'>logo或name</span>(需要主题支持)",
            "value": "name",
            "sort": 4
        },
        "APP_NAME": {
            "type": "string",
            "info": "APP(站点)名称,将作为全局变量使用在平台上",
            "value": "OSR DEMO",
            "sort": 1
        },
        "PC_LOGO_DISPLAY": {
            "type": "string",
            "info": "PC端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则显示Logo和App name<br>可填<span style='color:red;'>logo或name</span>(需要主题支持)",
            "value": "logo",
            "sort": 3
        },
        "__sort__": 1,
        "LOGO_IMG_URL_SECONDAEY": {
            "type": "string",
            "info": "APP(Web)Logo URL备用(需要主题支持)",
            "value": "/static/sys_imgs/osroom-logo-2.png",
            "sort": 5
        },
        "LOGO_IMG_URL": {
            "type": "string",
            "info": "APP(Web)Logo的URL",
            "value": "/static/sys_imgs/osroom-logo.png",
            "sort": 2
        },
        "__restart__": "not_must",
        "STATIC_FILE_VERSION": {
            "type": "int",
            "info": "静态文件版本(当修改了CSS,JS等静态文件的时候，修改此版本号)",
            "value": 20180404041316,
            "sort": 12
        },
        "TITLE_SUFFIX_ADM": {
            "type": "string",
            "info": "APP(Web)管理端Title后缀",
            "value": "OSROOM管理端",
            "sort": 9
        },
        "TITLE_PREFIX_ADM": {
            "type": "string",
            "info": "APP(Web)管理端Title前缀",
            "value": "",
            "sort": 7
        },
        "FRIEND_LINK": {
            "type": "dict",
            "info": "友情链接:值(Value)格式为{'url':'友情链接', 'logo_url':'logo链接'}",
            "value": {
                "阿里云": {
                    "aliases": "阿里云",
                    "icon_url": "",
                    "url": "www.aliyun.com",
                    "level": 1
                },
                "码云": {
                    "aliases": "码云",
                    "icon_url": "",
                    "url": "www.aliyun.com",
                    "level": 1
                },
                "七牛云": {
                    "aliases": "七牛云",
                    "icon_url": "",
                    "url": "www.aliyun.com",
                    "level": 1
                },
                "Github": {
                    "aliases": "Github",
                    "icon_url": "",
                    "url": "www.aliyun.com",
                    "level": 1
                }
            },
            "sort": 11
        },
        "SITE_URL": {
            "type": "string",
            "info": "Web站点URL(如果没有填写, 则使用默认的当前域名首页地址)",
            "value": "http://www.osroom.com",
            "sort": 11
        },
        "FAVICON": {
            "type": "string",
            "info": "APP(Web)favicon图标的URL",
            "value": "/static/sys_imgs/osroom-logo.ico",
            "sort": 10
        },
        "__info__": "基础设置: APP(Web)全局数据设置<br>此模块所有的KEY值, 都可以直接请求全局Api(/api/global)获取,也可以直接在主题中使用Jinjia2模板引擎获取(g.site_global.site_config.XXXX)",
        "TITLE_SUFFIX": {
            "type": "string",
            "info": "APP(Web)Title后缀",
            "value": "OSROOM开源Web DEMO",
            "sort": 8
        },
        "TITLE_PREFIX": {
            "type": "string",
            "info": "APP(Web)Title前缀",
            "value": "",
            "sort": 6
        }
    },
    "babel": {
        "__sort__": 9,
        "BABEL_DEFAULT_LOCALE": {
            "type": "string",
            "info": "默认语言:可以是zh_CN, en_US等()",
            "value": "zh_CN",
            "sort": 99
        },
        "__info__": "多语言设置",
        "LANGUAGES": {
            "type": "dict",
            "info": "管理端支持的语言",
            "value": {
                "en_US": {
                    "name": "English",
                    "alias": "En"
                },
                "zh_CN": {
                    "name": "中文",
                    "alias": "中文"
                }
            },
            "sort": 99
        },
        "__restart__": "must"
    },
    "email": {
        "MAIL_DEFAULT_SENDER": {
            "type": "list",
            "info": "默认发送者邮箱　(显示名称, 邮箱地址)顺序不能调换",
            "value": [
                "OSR DEMO",
                "system@osroom.com"
            ],
            "sort": 99
        },
        "MAIL_FOOTER": {
            "type": "string",
            "info": "发送邮件的页尾",
            "value": "OSROOM开源网站系统",
            "sort": 99
        },
        "APP_NAME": {
            "type": "string",
            "info": "在邮件中显示的APP(WEB)名称(1.不填写则不显示.2.如果主题邮件发送html模板不支持，也不显示)",
            "value": "OSR DEMO",
            "sort": 99
        },
        "__sort__": 10,
        "MAIL_USERNAME": {
            "type": "string",
            "info": "邮箱用户名",
            "value": "system@osroom.com",
            "sort": 99
        },
        "MAIL_PORT": {
            "type": "int",
            "info": "邮箱服务器端口",
            "value": 465,
            "sort": 99
        },
        "__restart__": "must",
        "MAIL_USE_TLS": {
            "type": "bool",
            "info": "是否使用TLS",
            "value": False,
            "sort": 99
        },
        "APP_LOG_URL": {
            "type": "string",
            "info": "在邮件中显示的LOGO图片URL(1.不填写则不显示.2.如果主题邮件发送html模板不支持，也不显示)",
            "value": "https://avatars1.githubusercontent.com/u/14039952?s=460&v=4",
            "sort": 99
        },
        "MAIL_SUBJECT_SUFFIX": {
            "type": "string",
            "info": "发送邮件的标题后缀",
            "value": "OSROOM",
            "sort": 99
        },
        "MAIL_PASSWORD": {
            "type": "password",
            "info": "邮箱密码, 是用于发送邮件的密码",
            "value": "<Your password>",
            "sort": 99
        },
        "__info__": "邮件发送参数设置（建议技术管理人员使用）",
        "MAIL_ASCII_ATTACHMENTS": {
            "type": "bool",
            "info": "MAIL ASCII ATTACHMENTS",
            "value": True,
            "sort": 99
        },
        "MAIL_SERVER": {
            "type": "string",
            "info": "邮箱服务器smtp",
            "value": "smtp.mxhichina.com",
            "sort": 99
        },
        "MAIL_USE_SSL": {
            "type": "bool",
            "info": "是否使用SSL",
            "value": True,
            "sort": 99
        }
    },
    "content_inspection": {
        "ALLEGED_ILLEGAL_SCORE": {
            "type": "float",
            "info": "内容检测分数高于多少分时属于涉嫌违规(0-100分,对于需要检查的内容有效)",
            "value": 99,
            "sort": 99
        },
        "AUDIO_OPEN": {
            "type": "bool",
            "info": "开启音频检测.需要hook_name为content_inspection_audio的音频检测插件",
            "value": False,
            "sort": 99
        },
        "IMAGE_OPEN": {
            "type": "bool",
            "info": "开启图片检测.需要hook_name为content_inspection_image的图片检测插件",
            "value": False,
            "sort": 99
        },
        "TEXT_OPEN": {
            "type": "bool",
            "info": "开启text检测.需要hook_name为content_inspection_text的文本检测插件",
            "value": True,
            "sort": 99
        },
        "__sort__": 5,
        "VEDIO_OPEN": {
            "type": "bool",
            "info": "开启视频检测.需要hook_name为content_inspection_vedio的视频检测插件",
            "value": False,
            "sort": 99
        },
        "__info__": "内容检查配置(需要安装相关插件该配置才生效).<br>检测开关:<br>1.如果开启, 并安装有相关的自动检查插件, 则会给发布的内容给出违规评分.如果未安装自动审核插件,则系统会给予评分100分(属涉嫌违规,网站工作人员账户除外).<br>2.如果关闭审核，则系统会给评分0分(不违规)",
        "__restart__": "not_must"
    },
    "account": {
        "USER_AVATAR_SIZE": {
            "type": "list",
            "info": "用户头像保存大小[<width>, <height>]像素",
            "value": [
                "360",
                "360"
            ],
            "sort": 99
        },
        "__sort__": 6,
        "USERNAME_MAX_LEN": {
            "type": "int",
            "info": "用户名最大长度",
            "value": 20,
            "sort": 99
        },
        "DEFAULT_AVATAR": {
            "type": "list",
            "info": "用户默认头像的URL,一般情况系统会选用第一个,随机头像时才会选用其他",
            "value": [
                "/static/admin/sys_imgs/avatar_default_1.png",
                "/static/admin/sys_imgs/avatar_default_2.png"
            ],
            "sort": 99
        },
        "__restart__": "not_must",
        "__info__": "账户设置"
    },
    "login_manager": {
        "PW_WRONG_NUM_IMG_CODE": {
            "type": "int",
            "info": "同一用户登录密码错误几次后响应图片验证码, 并且需要验证",
            "value": 5,
            "sort": 99
        },
        "LOGIN_OUT_TO": {
            "type": "string",
            "info": "退出登录后,api会响应数据会带上需要跳转到路由to_url:<LOGIN_OUT_TO>",
            "value": "/",
            "sort": 99
        },
        "LOGIN_VIEW": {
            "type": "string",
            "info": "需要登录的页面,未登录时,api会响应401,并带上需要跳转到路由to_url:<LOGIN_VIEW>",
            "value": "/sign-in",
            "sort": 99
        },
        "OPEN_REGISTER": {
            "type": "bool",
            "info": "开放注册",
            "value": True,
            "sort": 99
        },
        "__sort__": 99,
        "LOGIN_IN_TO": {
            "type": "string",
            "info": "登录成功后,api会响应数据会带上需要跳转到路由to_url:<LOGIN_IN_TO>",
            "value": "/",
            "sort": 99
        },
        "__info__": "在线管理（建议技术管理人员使用）",
        "__restart__": "not_must"
    },
    "permission": {
        "USER_MANAGE": {
            "type": "int",
            "info": "12b|用户类管理,包括Role, User",
            "value": 2048,
            "sort": 99
        },
        "STAFF": {
            "type": "int",
            "info": "8b|拥有此权重的用户被视为工作人员, 用法:如果比如一个需要SYS_SETTING权限才能查看的数据, 你可以自定义权限让STAFF可以使用GET请求方式(只开放查看)",
            "value": 128,
            "sort": 99
        },
        "EDITOR": {
            "type": "int",
            "info": "10b|管理端文字,图片编辑权重",
            "value": 512,
            "sort": 99
        },
        "__sort__": 99,
        "ROOT": {
            "type": "int",
            "info": "32b|超级管理, 有权控制ADMIN和IMPORTANT_DATA_DEL分配",
            "value": 2147483648,
            "sort": 99
        },
        "REPORT": {
            "type": "int",
            "info": "9b|报表查看权限",
            "value": 256,
            "sort": 99
        },
        "ADMIN": {
            "type": "int",
            "info": "28b|管理, 有权控制除ROOT,IMPORTANT_DATA_DEL外的其他角色分配",
            "value": 134217728,
            "sort": 99
        },
        "IMPORTANT_DATA_DEL": {
            "type": "int",
            "info": "30b|重要数据管理权限",
            "value": 536870912,
            "sort": 99
        },
        "FINANCE": {
            "type": "int",
            "info": "14b|财务, 涉及资金转账之类",
            "value": 8192,
            "sort": 99
        },
        "__info__": "权限设置[root用户才有权修改](建议技术管理人员使用）",
        "SYS_SETTING": {
            "type": "int",
            "info": "17b|网站系统设置",
            "value": 65536,
            "sort": 99
        },
        "WEB_SETTING": {
            "type": "int",
            "info": "16b|网站基础设置",
            "value": 32768,
            "sort": 99
        },
        "AUDIT": {
            "type": "int",
            "info": "11b|审核权限,主页针对普通用户发布的内容进行审核",
            "value": 1024,
            "sort": 99
        },
        "ORDER": {
            "type": "int",
            "info": "13b|订单管理权限",
            "value": 4096,
            "sort": 99
        },
        "DATA_MANAGE": {
            "type": "int",
            "info": "15b|网站数据管理, 涉及数据备份等",
            "value": 16384,
            "sort": 99
        },
        "USER": {
            "type": "int",
            "info": "1b|普通用户权重",
            "value": 1,
            "sort": 99
        },
        "__restart__": "not_must"
    },
    "py_venv": {
        "VENV_PATH": {
            "type": "string",
            "info": "\"python\"虚拟环境路径",
            "value": "/home/work/project/venv3",
            "sort": 99
        }
    },
    "user_model": {
        "__sort__": 99,
        "__info__": "用户Model",
        "EDITOR": {
            "type": "string",
            "info": "新用户默认编辑器类型rich_text或markdown",
            "value": "rich_text",
            "sort": 99
        },
        "__restart__": "not_must"
    },
    "seo": {
        "__restart__": "not_must",
        "__sort__": 4,
        "DEFAULT_DESCRIPTION": {
            "type": "string",
            "info": "网站的页面默认简单描述",
            "value": "开源Web系统, 可以作为企业网站, 个人博客网站, 微信小程序Web服务端",
            "sort": 99
        },
        "__info__": "简单的SEO配置<br>此模块所有的KEY值, 都可以直接请求全局Api(/api/global)获取,也可以直接在主题中使用Jinjia2模板引擎获取(g.site_global.site_config.XXXX)",
        "DEFAULT_KEYWORDS": {
            "type": "string",
            "info": "网站的页面默认关键词",
            "value": "开源, 企业网站, 博客网站, 微信小程序, Web服务端",
            "sort": 99
        }
    },
    "weblogger": {
        "USER_OP_LOG_KEEP_NUM": {
            "type": "int",
            "info": "用户操作日志保留个数",
            "value": 30,
            "sort": 99
        },
        "SING_IN_LOG_KEEP_NUM": {
            "type": "int",
            "info": "登录日志保留个数",
            "value": 30,
            "sort": 99
        },
        "__sort__": 99,
        "__info__": "操作日志设置",
        "__restart__": "not_must"
    },
    "theme": {
        "CURRENT_THEME_NAME": {
            "type": "string",
            "info": "当前主题名称,需与主题主目录名称相同",
            "value": "osr-style",
            "sort": 99
        },
        "__restart__": "not_must"
    }
}