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
    "user_model": {
        "__info__": "用户Model",
        "__sort__": 99,
        "__restart__": "not_must",
        "EDITOR": {
            "value": "rich_text",
            "info": "新用户默认编辑器类型rich_text或markdown",
            "sort": 99,
            "type": "string"
        }
    },
    "upload": {
        "__info__": "文件上传配置（建议技术管理人员使用）",
        "UP_ALLOWED_EXTENSIONS": {
            "value": [
                "txt",
                "xlxs",
                "excel",
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
            "info": "上传:允许上传的文件后缀(全部小写),每个用英文的','隔开",
            "sort": 99,
            "type": "list"
        },
        "__restart__": "not_must",
        "__sort__": 99,
        "IMG_VER_CODE_DIR": {
            "value": "verifi_code",
            "info": "系统生成的图片验证码保存目录",
            "sort": 99,
            "type": "string"
        },
        "SAVE_DIR": {
            "value": "media",
            "info": "上传:保存目录,如何存在'/'则会自动切分创建子目录",
            "sort": 99,
            "type": "string"
        }
    },
    "login_manager": {
        "__info__": "在线管理（建议技术管理人员使用）",
        "LOGIN_VIEW": {
            "value": "/sign-in",
            "info": "需要登录的页面,未登录时,api会响应401,并带上需要跳转到路由to_url:<LOGIN_VIEW>",
            "sort": 99,
            "type": "string"
        },
        "__restart__": "not_must",
        "LOGIN_OUT_TO": {
            "value": "/",
            "info": "退出登录后,api会响应数据会带上需要跳转到路由to_url:<LOGIN_OUT_TO>",
            "sort": 99,
            "type": "string"
        },
        "LOGIN_IN_TO": {
            "value": "/",
            "info": "登录成功后,api会响应数据会带上需要跳转到路由to_url:<LOGIN_IN_TO>",
            "sort": 99,
            "type": "string"
        },
        "__sort__": 99,
        "OPEN_REGISTER": {
            "value": True,
            "info": "开放注册",
            "sort": 99,
            "type": "bool"
        },
        "PW_WRONG_NUM_IMG_CODE": {
            "value": 5,
            "info": "同一用户登录密码错误几次后响应图片验证码, 并且需要验证",
            "sort": 99,
            "type": "int"
        }
    },
    "theme": {
        "CURRENT_THEME_NAME": {
            "value": "osr-style",
            "info": "当前主题名称,需与主题主目录名称相同",
            "sort": 99,
            "type": "string"
        }
    },
    "category": {
        "__info__": "Web参数设置",
        "CATEGORY_TYPE": {
            "value": {
                "其他类型库": "other",
                "图文|图库": "image",
                "视频库": "video",
                "音频库": "audio",
                "文本内容": "text",
                "文集": "post"
            },
            "info": "分类的品种只能有这几种",
            "sort": 99,
            "type": "dict"
        },
        "__restart__": "not_must",
        "__sort__": 7,
        "CATEGORY_MAX_LEN": {
            "value": 30,
            "info": "分类名称类型名最多几个字符",
            "sort": 99,
            "type": "int"
        }
    },
    "account": {
        "__info__": "账户设置",
        "__restart__": "not_must",
        "USER_AVATAR_SIZE": {
            "value": [
                "360",
                "360"
            ],
            "info": "用户头像保存大小[<width>, <height>]像素",
            "sort": 99,
            "type": "list"
        },
        "__sort__": 6,
        "DEFAULT_AVATAR": {
            "value": "/static/sys_imgs/avatar_default.png",
            "info": "新注册用户默认头像的URL",
            "sort": 99,
            "type": "string"
        },
        "USERNAME_MAX_LEN": {
            "value": 20,
            "info": "用户名最大长度",
            "sort": 99,
            "type": "int"
        }
    },
    "session": {
        "__info__": "Session参数设置（建议技术管理人员使用）",
        "SESSION_TYPE": {
            "value": "redis",
            "info": "保存Session会话的类型,可选mongodb, redis",
            "sort": 99,
            "type": "string"
        },
        "__restart__": "must",
        "SESSION_MONGODB_COLLECT": {
            "value": "osr_session",
            "info": "Mongodb保存session的collection,当SESSION_TYPE为mongodb时有效",
            "sort": 99,
            "type": "string"
        },
        "SESSION_KEY_PREFIX": {
            "value": "osr-session:",
            "info": "添加一个前缀,之前所有的会话密钥。这使得它可以为不同的应用程序使用相同的后端存储服务器",
            "sort": 99,
            "type": "string"
        },
        "__sort__": 99,
        "SESSION_PERMANENT": {
            "value": True,
            "info": "是否使用永久会话",
            "sort": 99,
            "type": "bool"
        },
        "PERMANENT_SESSION_LIFETIME": {
            "value": 2592000,
            "info": "永久会话的有效期.",
            "sort": 99,
            "type": "int"
        }
    },
    "seo": {
        "DEFAULT_KEYWORDS": {
            "value": "开源, 企业网站, 博客网站, 微信小程序, Web服务端",
            "info": "网站的页面默认关键词",
            "sort": 99,
            "type": "string"
        },
        "__info__": "简单的SEO配置<br>此模块所有的KEY值, 都可以直接请求全局Api(/api/global)获取,也可以直接在主题中使用Jinjia2模板引擎获取(g.site_global.site_config.XXXX)",
        "__sort__": 4,
        "__restart__": "not_must",
        "DEFAULT_DESCRIPTION": {
            "value": "开源Web系统, 可以作为企业网站, 个人博客网站, 微信小程序Web服务端",
            "info": "网站的页面默认简单描述",
            "sort": 99,
            "type": "string"
        }
    },
    "key": {
        "SECURITY_PASSWORD_SALT": {
            "value": "12343erfegrg",
            "info": "安全密码码盐值",
            "sort": 99,
            "type": "string"
        },
        "__info__": "安全Key（建议技术管理人员使用）",
        "__sort__": 99,
        "__restart__": "must",
        "SECRET_KEY": {
            "value": "12333r32fddvve",
            "info": "安全验证码",
            "sort": 99,
            "type": "string"
        }
    },
    "cache": {
        "__info__": "Web缓存参数设置（建议技术管理人员使用）",
        "__restart__": "must",
        "CACHE_KEY_PREFIX": {
            "value": "osr_cache",
            "info": "所有键(key)之前添加的前缀,这使得它可以为不同的应用程序使用相同的memcached(内存)服务器.",
            "sort": 99,
            "type": "string"
        },
        "CACHE_DEFAULT_TIMEOUT": {
            "value": 600,
            "info": "(s秒)默认缓存时间,当单个缓存没有设定缓存时间时会使用该时间",
            "sort": 99,
            "type": "int"
        },
        "CACHE_MONGODB_COLLECT": {
            "value": "osr_cache",
            "info": "保存cache的collection,当CACHE_TYPE为mongodb时有效",
            "sort": 99,
            "type": "string"
        },
        "__sort__": 99,
        "CACHE_TYPE": {
            "value": "redis",
            "info": "缓存使用的类型,可选择redis,mongodb",
            "sort": 99,
            "type": "string"
        },
        "USE_CACHE": {
            "value": True,
            "info": "是否使用缓存功能,建议开启",
            "sort": 99,
            "type": "bool"
        }
    },
    "weblogger": {
        "USER_OP_LOG_KEEP_NUM": {
            "value": 30,
            "info": "用户操作日志保留个数",
            "sort": 99,
            "type": "int"
        },
        "__info__": "操作日志设置",
        "__sort__": 99,
        "__restart__": "not_must",
        "SING_IN_LOG_KEEP_NUM": {
            "value": 30,
            "info": "登录日志保留个数",
            "sort": 99,
            "type": "int"
        }
    },
    "permission": {
        "SYS_SETTING": {
            "value": 65536,
            "info": "17b|网站系统设置",
            "sort": 99,
            "type": "int"
        },
        "ADMIN": {
            "value": 134217728,
            "info": "28b|管理, 有权控制除ROOT,IMPORTANT_DATA_DEL外的其他角色分配",
            "sort": 99,
            "type": "int"
        },
        "WEB_SETTING": {
            "value": 32768,
            "info": "16b|网站基础设置",
            "sort": 99,
            "type": "int"
        },
        "DATA_MANAGE": {
            "value": 16384,
            "info": "15b|网站数据管理, 涉及数据备份等",
            "sort": 99,
            "type": "int"
        },
        "REPORT": {
            "value": 256,
            "info": "9b|报表查看权限",
            "sort": 99,
            "type": "int"
        },
        "EDITOR": {
            "value": 512,
            "info": "10b|管理端文字,图片编辑权重",
            "sort": 99,
            "type": "int"
        },
        "__sort__": 99,
        "__info__": "权限设置[root用户才有权修改](建议技术管理人员使用）",
        "STAFF": {
            "value": 128,
            "info": "8b|拥有此权重的用户被视为工作人员, 用法:如果比如一个需要SYS_SETTING权限才能查看的数据, 你可以自定义权限让STAFF可以使用GET请求方式(只开放查看)",
            "sort": 99,
            "type": "int"
        },
        "USER": {
            "value": 1,
            "info": "1b|普通用户权重",
            "sort": 99,
            "type": "int"
        },
        "IMPORTANT_DATA_DEL": {
            "value": 536870912,
            "info": "30b|重要数据管理权限",
            "sort": 99,
            "type": "int"
        },
        "FINANCE": {
            "value": 8192,
            "info": "14b|财务, 涉及资金转账之类",
            "sort": 99,
            "type": "int"
        },
        "ORDER": {
            "value": 4096,
            "info": "13b|订单管理权限",
            "sort": 99,
            "type": "int"
        },
        "__restart__": "not_must",
        "USER_MANAGE": {
            "value": 2048,
            "info": "12b|用户类管理,包括Role, User",
            "sort": 99,
            "type": "int"
        },
        "ROOT": {
            "value": 2147483648,
            "info": "32b|超级管理, 有权控制ADMIN和IMPORTANT_DATA_DEL分配",
            "sort": 99,
            "type": "int"
        },
        "AUDIT": {
            "value": 1024,
            "info": "11b|审核权限,主页针对普通用户发布的内容进行审核",
            "sort": 99,
            "type": "int"
        }
    },
    "name_audit": {
        "__info__": "名称验证, 如用户名,分类名称",
        "AUDIT_PROJECT_KEY": {
            "value": {
                "class_name": "审核一些短的分类名称, 如category, tag",
                "username": "审核用户名"
            },
            "info": "审核项目的Key(键),审核时会使用一个Key来获取审核规则,正则去匹配用户输入的内容",
            "sort": 99,
            "type": "dict"
        },
        "__restart__": "not_must",
        "__sort__": 8
    },
    "site_config": {
        "LOGO_IMG_URL": {
            "value": "https://osroom-test2.oss-cn-shenzhen.aliyuncs.com/multimedia/image/a82d6b56-3fa9-11e8-bff8-001c42462937.png",
            "info": "APP(Web)Logo的URL",
            "sort": 2,
            "type": "string"
        },
        "__info__": "基础设置: APP(Web)全局数据设置<br>此模块所有的KEY值, 都可以直接请求全局Api(/api/global)获取,也可以直接在主题中使用Jinjia2模板引擎获取(g.site_global.site_config.XXXX)",
        "HEAD_CODE": {
            "value": "",
            "info": "用于放入html中哦你head标签内的js/css/html代码(如Google分析代码/百度统计代码)",
            "sort": 13,
            "type": "string"
        },
        "TITLE_PREFIX": {
            "value": "",
            "info": "APP(Web)Title前缀",
            "sort": 6,
            "type": "string"
        },
        "__sort__": 1,
        "FRIEND_LINK": {
            "value": {
                "Github": {
                    "url": "https://github.com/osroom/osroom",
                    "logo_url": "http://osr.local.com:5000/static/admin/sys_imgs/osroom-logo-1.png?w=240&h=240"
                },
                "Aliyun": {
                    "url": "https://github.com/osroom/osroom",
                    "logo_url": "http://osr.local.com:5000/static/admin/sys_imgs/osroom-logo-1.png?w=240&h=240"
                },
                "Qiniu": {
                    "url": "https://github.com/osroom/osroom",
                    "logo_url": "http://osr.local.com:5000/static/admin/sys_imgs/osroom-logo-1.png?w=240&h=240"
                },
                "VueJS": {
                    "url": "https://github.com/osroom/osroom",
                    "logo_url": "http://osr.local.com:5000/static/admin/sys_imgs/osroom-logo-1.png?w=240&h=240"
                }
            },
            "info": "友情链接:值(Value)格式为{'url':'友情链接', 'logo_url':'logo链接'}",
            "sort": 11,
            "type": "dict"
        },
        "SITE_URL": {
            "value": "http://www.osroom.com",
            "info": "Web站点URL(如果没有填写, 则使用默认的当前域名首页地址)",
            "sort": 11,
            "type": "string"
        },
        "LOGO_IMG_URL_SECONDAEY": {
            "value": "https://osroom-test2.oss-cn-shenzhen.aliyuncs.com/multimedia/image/84f39b6a-470c-11e8-bff8-001c42462937.png",
            "info": "APP(Web)Logo URL备用(需要主题支持)",
            "sort": 5,
            "type": "string"
        },
        "STATIC_FILE_VERSION": {
            "value": 20180510123300,
            "info": "静态文件版本(当修改了CSS,JS等静态文件的时候，修改此版本号)",
            "sort": 12,
            "type": "int"
        },
        "TITLE_SUFFIX_ADM": {
            "value": "OSROOM管理端",
            "info": "APP(Web)管理端Title后缀",
            "sort": 9,
            "type": "string"
        },
        "APP_NAME": {
            "value": "OSR DEMO",
            "info": "APP(站点)名称,将作为全局变量使用在平台上",
            "sort": 1,
            "type": "string"
        },
        "__restart__": "not_must",
        "TITLE_SUFFIX": {
            "value": "OSROOM开源Web DEMO",
            "info": "APP(Web)Title后缀",
            "sort": 8,
            "type": "string"
        },
        "PC_LOGO_DISPLAY": {
            "value": "logo",
            "info": "PC端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则显示Logo和App name<br>可填logo或name(需要主题支持)",
            "sort": 3,
            "type": "string"
        },
        "TITLE_PREFIX_ADM": {
            "value": "",
            "info": "APP(Web)管理端Title前缀",
            "sort": 7,
            "type": "string"
        },
        "MB_LOGO_DISPLAY": {
            "value": "logo",
            "info": "移动端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则App name优先<br>可填logo或name(需要主题支持)",
            "sort": 4,
            "type": "string"
        },
        "FAVICON": {
            "value": "https://osroom-test2.oss-cn-shenzhen.aliyuncs.com/multimedia/image/0220d5b6-4321-11e8-bff8-001c42462937.ico",
            "info": "APP(Web)favicon图标的URL",
            "sort": 10,
            "type": "string"
        }
    },
    "py_venv": {
        "VENV_PATH": {
            "value": "/home/work/project/venv3",
            "info": "\"python\"虚拟环境路径",
            "sort": 99,
            "type": "string"
        }
    },
    "rest_auth_token": {
        "__info__": "Web参数设置",
        "__sort__": 99,
        "__restart__": "not_must",
        "LOGIN_LIFETIME": {
            "value": 2592000,
            "info": "jwt 登录BearerToken有效期(s)",
            "sort": 99,
            "type": "int"
        },
        "MAX_SAME_TIME_LOGIN": {
            "value": 3,
            "info": "最多能同时登录几个使用JWT验证的客户端,超过此数目则会把旧的登录注销",
            "sort": 99,
            "type": "int"
        },
        "REST_ACCESS_TOKEN_LIFETIME": {
            "value": 172800,
            "info": "给客户端发补的访问Token AccessToken的有效期",
            "sort": 99,
            "type": "int"
        }
    },
    "content_inspection": {
        "__info__": "内容检查配置(需要安装相关插件该配置才生效).<br>检测开关:<br>1.如果开启, 并安装有相关的自动检查插件, 则会给发布的内容给出违规评分.如果未安装自动审核插件,则系统会给予评分100分(属涉嫌违规,网站工作人员账户除外).<br>2.如果关闭审核，则系统会给评分0分(不违规)",
        "AUDIO_OPEN": {
            "value": False,
            "info": "开启音频检测.需要hook_name为content_inspection_audio的音频检测插件",
            "sort": 99,
            "type": "bool"
        },
        "TEXT_OPEN": {
            "value": True,
            "info": "开启text检测.需要hook_name为content_inspection_text的文本检测插件",
            "sort": 99,
            "type": "bool"
        },
        "ALLEGED_ILLEGAL_SCORE": {
            "value": 99,
            "info": "内容检测分数高于多少分时属于涉嫌违规(0-100分,对于需要检查的内容有效)",
            "sort": 99,
            "type": "float"
        },
        "__restart__": "not_must",
        "__sort__": 5,
        "IMAGE_OPEN": {
            "value": False,
            "info": "开启图片检测.需要hook_name为content_inspection_image的图片检测插件",
            "sort": 99,
            "type": "bool"
        },
        "VEDIO_OPEN": {
            "value": False,
            "info": "开启视频检测.需要hook_name为content_inspection_vedio的视频检测插件",
            "sort": 99,
            "type": "bool"
        }
    },
    "email": {
        "MAIL_PORT": {
            "value": 465,
            "info": "邮箱服务器端口",
            "sort": 99,
            "type": "int"
        },
        "__info__": "邮件发送参数设置（建议技术管理人员使用）",
        "__sort__": 10,
        "MAIL_FOOTER": {
            "value": "OSROOM开源网站系统www.osroom.com",
            "info": "发送邮件的页尾",
            "sort": 99,
            "type": "string"
        },
        "APP_LOG_URL": {
            "value": "https://osroom-test2.oss-cn-shenzhen.aliyuncs.com/multimedia/image/a82d6b56-3fa9-11e8-bff8-001c42462937.png",
            "info": "在邮件中显示的LOGO图片URL(1.不填写则不显示.2.如果主题邮件发送html模板不支持，也不显示)",
            "sort": 99,
            "type": "string"
        },
        "MAIL_USERNAME": {
            "value": "system@osroom.com",
            "info": "邮箱用户名",
            "sort": 99,
            "type": "string"
        },
        "APP_NAME": {
            "value": "",
            "info": "在邮件中显示的APP(WEB)名称(1.不填写则不显示.2.如果主题邮件发送html模板不支持，也不显示)",
            "sort": 99,
            "type": "string"
        },
        "MAIL_DEFAULT_SENDER": {
            "value": [
                "OSR DEMO",
                "system@osroom.com"
            ],
            "info": "默认发送者邮箱　(显示名称, 邮箱地址)顺序不能调换",
            "sort": 99,
            "type": "list"
        },
        "MAIL_USE_TLS": {
            "value": False,
            "info": "是否使用TLS",
            "sort": 99,
            "type": "bool"
        },
        "MAIL_ASCII_ATTACHMENTS": {
            "value": True,
            "info": "MAIL ASCII ATTACHMENTS",
            "sort": 99,
            "type": "bool"
        },
        "__restart__": "must",
        "MAIL_SERVER": {
            "value": "smtp.mxhichina.com",
            "info": "邮箱服务器smtp",
            "sort": 99,
            "type": "string"
        },
        "MAIL_USE_SSL": {
            "value": True,
            "info": "是否使用SSL",
            "sort": 99,
            "type": "bool"
        },
        "MAIL_SUBJECT_SUFFIX": {
            "value": "OSROOM",
            "info": "发送邮件的标题后缀",
            "sort": 99,
            "type": "string"
        },
        "MAIL_PASSWORD": {
            "value": "<Your password>",
            "info": "邮箱密码, 是用于发送邮件的密码",
            "sort": 99,
            "type": "password"
        }
    },
    "system": {
        "__restart__": "must",
        "__info__": "其他web系统参数设置（建议技术管理人员使用）",
        "__sort__": 99,
        "TEMPLATES_AUTO_RELOAD": {
            "value": True,
            "info": "是否自动加载页面(html)模板.开启后,每次html页面修改都无需重启Web",
            "sort": 99,
            "type": "bool"
        }
    },
    "comment": {
        "NUM_PAGE": {
            "value": 10,
            "info": "每个页面获取几条评论, 如果请求获取评论时指定了指定了per参数, 则此配置无效(此配置也对管理端无效)",
            "sort": 99,
            "type": "int"
        },
        "__info__": "评论内容设置",
        "INTERVAL": {
            "value": 30,
            "info": "控制评论频繁度时间(s)",
            "sort": 99,
            "type": "int"
        },
        "__restart__": "not_must",
        "NUM_OF_INTERVAL": {
            "value": 3,
            "info": "控制评论频繁度时间内最多评论几次",
            "sort": 99,
            "type": "int"
        },
        "TRAVELER_COMMENT": {
            "value": False,
            "info": "游客评论开关,是否打开?",
            "sort": 99,
            "type": "bool"
        },
        "NUM_PAGE_MAX": {
            "value": 30,
            "info": "每个页面最多获取几条评论(此配置对管理端无效)",
            "sort": 99,
            "type": "int"
        },
        "__sort__": 3,
        "OPEN_COMMENT": {
            "value": True,
            "info": "评论开关,是否打开评论功能?",
            "sort": 99,
            "type": "bool"
        },
        "MAX_LEN": {
            "value": 300,
            "info": "发布评论最多几个字符",
            "sort": 99,
            "type": "int"
        }
    },
    "babel": {
        "BABEL_DEFAULT_LOCALE": {
            "value": "zh_CN",
            "info": "默认语言:可以是zh_CN, en_US等()",
            "sort": 99,
            "type": "string"
        },
        "__info__": "多语言设置",
        "__sort__": 9,
        "__restart__": "must",
        "LANGUAGES": {
            "value": {
                "en_US": {
                    "alias": "En",
                    "name": "English"
                },
                "zh_CN": {
                    "alias": "中文",
                    "name": "中文"
                }
            },
            "info": "管理端支持的语言",
            "sort": 99,
            "type": "dict"
        }
    },
    "post": {
        "TITLE_MAX_LEN": {
            "value": 50,
            "info": "文章Title最大长度",
            "sort": 99,
            "type": "int"
        },
        "NUM_PAGE": {
            "value": 15,
            "info": "每个页面获取几篇文章, 如果请求获取文章时指定了指定了per参数, 则此配置无效(此配置也对管理端无效)",
            "sort": 99,
            "type": "int"
        },
        "__info__": "文章内容设置",
        "NUM_PAGE_MAX": {
            "value": 30,
            "info": "每个页面最多获取几篇文章(此配置对管理端无效)",
            "sort": 99,
            "type": "int"
        },
        "__restart__": "not_must",
        "TAG_MAX_LEN": {
            "value": 10,
            "info": "POST标签最多几个字",
            "sort": 99,
            "type": "int"
        },
        "BRIEF_LEN": {
            "value": 80,
            "info": "获取文章简要的字数",
            "sort": 99,
            "type": "int"
        },
        "MAX_LEN": {
            "value": 5000,
            "info": "发布文章最多几个字符",
            "sort": 99,
            "type": "int"
        },
        "__sort__": 2,
        "TAG_MAX_NUM": {
            "value": 5,
            "info": "POST标签最大个数",
            "sort": 99,
            "type": "int"
        }
    },
    "verify_code": {
        "EXPIRATION": {
            "value": 600,
            "info": "验证码过期时间(s)",
            "sort": 99,
            "type": "int"
        },
        "__info__": "验证码(建议技术管理员配置)",
        "__restart__": "not_must",
        "SEND_CODE_TYPE": {
            "value": {
                "string": 0,
                "int": 6
            },
            "info": "发送的验证码字符类型，与字符个数",
            "sort": 99,
            "type": "dict"
        },
        "MAX_IMG_CODE_INTERFERENCE": {
            "value": 40,
            "info": "图片验证码干扰程度的最大值",
            "sort": 99,
            "type": "int"
        },
        "__sort__": 11,
        "MAX_NUM_SEND_SAMEIP_PERMIN_NO_IMGCODE": {
            "value": 1,
            "info": "同一IP地址,同一用户(未登录的同属同一匿名用户),允许每分钟在不验证[图片验证码]的时候,调用API发送验证码最大次数.超过次数后API会生成[图片验证码]并返回图片url对象(也可以自己调用获取图片验证码API获取).如果你的客户端(包括主题)不支持显示图片验证码,请设置此配置为99999999",
            "sort": 99,
            "type": "int"
        },
        "MAX_NUM_SEND_SAMEIP_PERMIN": {
            "value": 15,
            "info": "同一IP地址,同一用户(未登录的同属一匿名用户), 允许每分钟调用API发送验证码的最大次数",
            "sort": 99,
            "type": "int"
        },
        "MIN_IMG_CODE_INTERFERENCE": {
            "value": 10,
            "info": "图片验证码干扰程度的最小值,最小值小于10时无效",
            "sort": 99,
            "type": "int"
        },
        "IMG_CODE_DIR": {
            "value": "admin/verify_code",
            "info": "图片验证码保存目录",
            "sort": 99,
            "type": "string"
        }
    }
}