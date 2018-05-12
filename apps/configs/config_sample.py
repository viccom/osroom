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
配置表,表中没有__restart__的项目将不会出现在管理端的设置中
###############################################################################
'''
# Danger: If True, the database configuration data will be overwritten
# 危险:如果为True, 则会把该文件配置覆盖掉数据库中保存的配置
OVERWRITE_DB = False
CONFIG = {
    "comment": {
        "INTERVAL": {
            "type": "int",
            "sort": 99,
            "info": "控制评论频繁度时间(s)",
            "value": 30
        },
        "__sort__": 3,
        "__info__": "评论内容设置",
        "OPEN_COMMENT": {
            "type": "bool",
            "sort": 99,
            "info": "评论开关,是否打开评论功能?",
            "value": True
        },
        "NUM_OF_INTERVAL": {
            "type": "int",
            "sort": 99,
            "info": "控制评论频繁度时间内最多评论几次",
            "value": 3
        },
        "NUM_PAGE": {
            "type": "int",
            "sort": 99,
            "info": "每个页面获取几条评论, 如果请求获取评论时指定了指定了per参数, 则此配置无效(此配置也对管理端无效)",
            "value": 10
        },
        "__restart__": "not_must",
        "MAX_LEN": {
            "type": "int",
            "sort": 99,
            "info": "发布评论最多几个字符",
            "value": 300
        },
        "NUM_PAGE_MAX": {
            "type": "int",
            "sort": 99,
            "info": "每个页面最多获取几条评论(此配置对管理端无效)",
            "value": 30
        },
        "TRAVELER_COMMENT": {
            "type": "bool",
            "sort": 99,
            "info": "游客评论开关,是否打开?",
            "value": False
        }
    },
    "name_audit": {
        "__restart__": "not_must",
        "__sort__": 8,
        "__info__": "名称验证, 如用户名,分类名称",
        "AUDIT_PROJECT_KEY": {
            "type": "dict",
            "sort": 99,
            "info": "审核项目的Key(键),审核时会使用一个Key来获取审核规则,正则去匹配用户输入的内容",
            "value": {
                "username": "审核用户名",
                "class_name": "审核一些短的分类名称, 如category, tag"
            }
        }
    },
    "content_inspection": {
        "ALLEGED_ILLEGAL_SCORE": {
            "type": "float",
            "sort": 99,
            "info": "内容检测分数高于多少分时属于涉嫌违规(0-100分,对于需要检查的内容有效)",
            "value": 99
        },
        "TEXT_OPEN": {
            "type": "bool",
            "sort": 99,
            "info": "开启text检测.需要hook_name为content_inspection_text的文本检测插件",
            "value": True
        },
        "__sort__": 5,
        "__info__": "内容检查配置(需要安装相关插件该配置才生效).<br>检测开关:<br>1.如果开启, 并安装有相关的自动检查插件, 则会给发布的内容给出违规评分.如果未安装自动审核插件,则系统会给予评分100分(属涉嫌违规,网站工作人员账户除外).<br>2.如果关闭审核，则系统会给评分0分(不违规)",
        "__restart__": "not_must",
        "AUDIO_OPEN": {
            "type": "bool",
            "sort": 99,
            "info": "开启音频检测.需要hook_name为content_inspection_audio的音频检测插件",
            "value": False
        },
        "VEDIO_OPEN": {
            "type": "bool",
            "sort": 99,
            "info": "开启视频检测.需要hook_name为content_inspection_vedio的视频检测插件",
            "value": False
        },
        "IMAGE_OPEN": {
            "type": "bool",
            "sort": 99,
            "info": "开启图片检测.需要hook_name为content_inspection_image的图片检测插件",
            "value": False
        }
    },
    "verify_code": {
        "MAX_NUM_SEND_SAMEIP_PERMIN_NO_IMGCODE": {
            "type": "int",
            "sort": 99,
            "info": "同一IP地址,同一用户(未登录的同属同一匿名用户),允许每分钟在不验证[图片验证码]的时候,调用API发送验证码最大次数.<br>超过次数后API会生成[图片验证码]并返回图片url对象(也可以自己调用获取图片验证码API获取).<br>如果你的客户端(包括主题)不支持显示图片验证码,请设置此配置为99999999",
            "value": 1
        },
        "EXPIRATION": {
            "type": "int",
            "sort": 99,
            "info": "验证码过期时间(s)",
            "value": 600
        },
        "__sort__": 11,
        "__info__": "验证码(建议技术管理员配置)",
        "SEND_CODE_TYPE": {
            "type": "dict",
            "sort": 99,
            "info": "发送的验证码字符类型，与字符个数",
            "value": {
                "string": 0,
                "int": 6
            }
        },
        "MIN_IMG_CODE_INTERFERENCE": {
            "type": "int",
            "sort": 99,
            "info": "图片验证码干扰程度的最小值,最小值小于10时无效",
            "value": 10
        },
        "IMG_CODE_DIR": {
            "type": "string",
            "sort": 99,
            "info": "图片验证码保存目录",
            "value": "admin/verify_code"
        },
        "__restart__": "not_must",
        "MAX_IMG_CODE_INTERFERENCE": {
            "type": "int",
            "sort": 99,
            "info": "图片验证码干扰程度的最大值",
            "value": 40
        },
        "MAX_NUM_SEND_SAMEIP_PERMIN": {
            "type": "int",
            "sort": 99,
            "info": "同一IP地址,同一用户(未登录的同属一匿名用户), 允许每分钟调用API发送验证码的最大次数",
            "value": 15
        }
    },
    "account": {
        "__sort__": 6,
        "__info__": "账户设置",
        "DEFAULT_AVATAR": {
            "type": "string",
            "sort": 99,
            "info": "新注册用户默认头像的URL",
            "value": "/static/sys_imgs/avatar_default.png"
        },
        "__restart__": "not_must",
        "USERNAME_MAX_LEN": {
            "type": "int",
            "sort": 99,
            "info": "用户名最大长度",
            "value": 20
        },
        "USER_AVATAR_MAX_SIZE": {
            "type": "float",
            "sort": 99,
            "info": "用户头像不能上传超过此值大小(单位Mb)的图片作头像",
            "value": 10.0
        },
        "USER_AVATAR_SIZE": {
            "type": "list",
            "sort": 99,
            "info": "用户头像保存大小[<width>, <height>]像素",
            "value": [
                "360",
                "360"
            ]
        }
    },
    "system": {
        "__sort__": 99,
        "__info__": "其他web系统参数设置（建议技术管理人员使用）",
        "KEY_HIDING": {
            "type": "bool",
            "sort": 2,
            "info": "开启后,管理端通过/api/admin/xxx获取到的数据中，密钥类型的值，则会以随机字符代替.<br><span style='color:red;'>如某个插件配置中有密码, 不想让它暴露在浏览器, 则可开启.</span>",
            "value": False
        },
        "__restart__": "must",
        "MAX_CONTENT_LENGTH": {
            "type": "float",
            "sort": 1,
            "info": "拒绝内容长度大于此值的请求进入，并返回一个 413 状态码(单位:Mb)",
            "value": 50.0
        },
        "TEMPLATES_AUTO_RELOAD": {
            "type": "bool",
            "sort": 3,
            "info": "是否自动加载页面(html)模板.开启后,每次html页面修改都无需重启Web",
            "value": True
        }
    },
    "theme": {
        "CURRENT_THEME_NAME": {
            "type": "string",
            "sort": 99,
            "info": "当前主题名称,需与主题主目录名称相同",
            "value": "osr-style"
        }
    },
    "py_venv": {
        "VENV_PATH": {
            "type": "string",
            "sort": 99,
            "info": "python虚拟环境路径",
            "value": "/home/work/project/venv3"
        }
    },
    "key": {
        "__restart__": "must",
        "SECURITY_PASSWORD_SALT": {
            "type": "string",
            "sort": 99,
            "info": "安全密码码盐值",
            "value": "12343erfegrg"
        },
        "__sort__": 99,
        "__info__": "安全Key（建议技术管理人员使用）",
        "SECRET_KEY": {
            "type": "string",
            "sort": 99,
            "info": "安全验证码",
            "value": "12333r32fddvve"
        }
    },
    "category": {
        "__restart__": "not_must",
        "__sort__": 7,
        "__info__": "Web参数设置",
        "CATEGORY_MAX_LEN": {
            "type": "int",
            "sort": 99,
            "info": "分类名称类型名最多几个字符",
            "value": 30
        },
        "CATEGORY_TYPE": {
            "type": "dict",
            "sort": 99,
            "info": "分类的品种只能有这几种",
            "value": {
                "音频库": "audio",
                "文本内容": "text",
                "其他类型库": "other",
                "文集": "post",
                "视频库": "video",
                "图文|图库": "image"
            }
        }
    },
    "rest_auth_token": {
        "__sort__": 99,
        "__info__": "Web参数设置",
        "MAX_SAME_TIME_LOGIN": {
            "type": "int",
            "sort": 99,
            "info": "最多能同时登录几个使用JWT验证的客户端,超过此数目则会把旧的登录注销",
            "value": 3
        },
        "__restart__": "not_must",
        "REST_ACCESS_TOKEN_LIFETIME": {
            "type": "int",
            "sort": 99,
            "info": "给客户端发补的访问Token AccessToken的有效期",
            "value": 172800
        },
        "LOGIN_LIFETIME": {
            "type": "int",
            "sort": 99,
            "info": "jwt 登录BearerToken有效期(s)",
            "value": 2592000
        }
    },
    "post": {
        "TAG_MAX_NUM": {
            "type": "int",
            "sort": 99,
            "info": "POST标签最大个数",
            "value": 5
        },
        "TITLE_MAX_LEN": {
            "type": "int",
            "sort": 99,
            "info": "文章Title最大长度",
            "value": 50
        },
        "NUM_PAGE_MAX": {
            "type": "int",
            "sort": 99,
            "info": "每个页面最多获取几篇文章(此配置对管理端无效)",
            "value": 30
        },
        "TAG_MAX_LEN": {
            "type": "int",
            "sort": 99,
            "info": "POST标签最多几个字",
            "value": 10
        },
        "BRIEF_LEN": {
            "type": "int",
            "sort": 99,
            "info": "获取文章简要的字数",
            "value": 80
        },
        "NUM_PAGE": {
            "type": "int",
            "sort": 99,
            "info": "每个页面获取几篇文章, 如果请求获取文章时指定了指定了per参数, 则此配置无效(此配置也对管理端无效)",
            "value": 15
        },
        "__restart__": "not_must",
        "MAX_LEN": {
            "type": "int",
            "sort": 99,
            "info": "发布文章最多几个字符",
            "value": 5000
        },
        "__sort__": 2,
        "GET_POST_CACHE_TIME_OUT": {
            "type": "int",
            "sort": 99,
            "info": "获取多个post数据时, 缓存超时时间(s), 为0表示不缓存数据.<br><span style='color:red;'>只对获取已公开发布的, 并且不是当前用户发布的post有效</span>",
            "value": 60
        },
        "__info__": "文章内容设置"
    },
    "permission": {
        "__sort__": 99,
        "__info__": "权限设置[root用户才有权修改](建议技术管理人员使用）",
        "FINANCE": {
            "type": "int",
            "sort": 99,
            "info": "14b|财务, 涉及资金转账之类",
            "value": 8192
        },
        "IMPORTANT_DATA_DEL": {
            "type": "int",
            "sort": 99,
            "info": "30b|重要数据管理权限",
            "value": 536870912
        },
        "REPORT": {
            "type": "int",
            "sort": 99,
            "info": "9b|报表查看权限",
            "value": 256
        },
        "DATA_MANAGE": {
            "type": "int",
            "sort": 99,
            "info": "15b|网站数据管理, 涉及数据备份等",
            "value": 16384
        },
        "ROOT": {
            "type": "int",
            "sort": 99,
            "info": "32b|超级管理, 有权控制ADMIN和IMPORTANT_DATA_DEL分配",
            "value": 2147483648
        },
        "__restart__": "not_must",
        "USER": {
            "type": "int",
            "sort": 99,
            "info": "1b|普通用户权重",
            "value": 1
        },
        "AUDIT": {
            "type": "int",
            "sort": 99,
            "info": "11b|审核权限,主页针对普通用户发布的内容进行审核",
            "value": 1024
        },
        "ORDER": {
            "type": "int",
            "sort": 99,
            "info": "13b|订单管理权限",
            "value": 4096
        },
        "ADMIN": {
            "type": "int",
            "sort": 99,
            "info": "28b|管理, 有权控制除ROOT,IMPORTANT_DATA_DEL外的其他角色分配",
            "value": 134217728
        },
        "EDITOR": {
            "type": "int",
            "sort": 99,
            "info": "10b|管理端文字,图片编辑权重",
            "value": 512
        },
        "USER_MANAGE": {
            "type": "int",
            "sort": 99,
            "info": "12b|用户类管理,包括Role, User",
            "value": 2048
        },
        "WEB_SETTING": {
            "type": "int",
            "sort": 99,
            "info": "16b|网站基础设置",
            "value": 32768
        },
        "STAFF": {
            "type": "int",
            "sort": 99,
            "info": "8b|拥有此权重的用户被视为工作人员, 用法:如果比如一个需要SYS_SETTING权限才能查看的数据, 你可以自定义权限让STAFF可以使用GET请求方式(只开放查看)",
            "value": 128
        },
        "SYS_SETTING": {
            "type": "int",
            "sort": 99,
            "info": "17b|网站系统设置",
            "value": 65536
        }
    },
    "session": {
        "PERMANENT_SESSION_LIFETIME": {
            "type": "int",
            "sort": 99,
            "info": "永久会话的有效期.",
            "value": 2592000
        },
        "__sort__": 99,
        "__info__": "Session参数设置（建议技术管理人员使用）",
        "__restart__": "must",
        "SESSION_TYPE": {
            "type": "string",
            "sort": 99,
            "info": "保存Session会话的类型,可选mongodb, redis",
            "value": "redis"
        },
        "SESSION_PERMANENT": {
            "type": "bool",
            "sort": 99,
            "info": "是否使用永久会话",
            "value": True
        },
        "SESSION_MONGODB_COLLECT": {
            "type": "string",
            "sort": 99,
            "info": "Mongodb保存session的collection,当SESSION_TYPE为mongodb时有效",
            "value": "osr_session"
        },
        "SESSION_KEY_PREFIX": {
            "type": "string",
            "sort": 99,
            "info": "添加一个前缀,之前所有的会话密钥。这使得它可以为不同的应用程序使用相同的后端存储服务器",
            "value": "osr-session:"
        }
    },
    "user_model": {
        "__restart__": "not_must",
        "__sort__": 99,
        "__info__": "用户Model",
        "EDITOR": {
            "type": "string",
            "sort": 99,
            "info": "新用户默认编辑器类型rich_text或markdown",
            "value": "rich_text"
        }
    },
    "login_manager": {
        "OPEN_REGISTER": {
            "type": "bool",
            "sort": 99,
            "info": "开放注册",
            "value": True
        },
        "__sort__": 99,
        "__info__": "在线管理（建议技术管理人员使用）",
        "LOGIN_IN_TO": {
            "type": "string",
            "sort": 99,
            "info": "登录成功后,api会响应数据会带上需要跳转到路由to_url",
            "value": "/"
        },
        "__restart__": "not_must",
        "LOGIN_OUT_TO": {
            "type": "string",
            "sort": 99,
            "info": "退出登录后,api会响应数据会带上需要跳转到路由to_url",
            "value": "/"
        },
        "LOGIN_VIEW": {
            "type": "string",
            "sort": 99,
            "info": "需要登录的页面,未登录时,api会响应401,并带上需要跳转到路由to_url",
            "value": "/sign-in"
        },
        "PW_WRONG_NUM_IMG_CODE": {
            "type": "int",
            "sort": 99,
            "info": "同一用户登录密码错误几次后响应图片验证码, 并且需要验证",
            "value": 5
        }
    },
    "email": {
        "APP_LOG_URL": {
            "type": "string",
            "sort": 99,
            "info": "在邮件中显示的LOGO图片URL(1.不填写则不显示.2.如果主题邮件发送html模板不支持，也不显示)",
            "value": "/static/sys_imgs/osroom-logo.png"
        },
        "MAIL_USERNAME": {
            "type": "string",
            "sort": 99,
            "info": "邮箱用户名",
            "value": "system@osroom.com"
        },
        "MAIL_USE_TLS": {
            "type": "bool",
            "sort": 99,
            "info": "是否使用TLS",
            "value": False
        },
        "MAIL_SERVER": {
            "type": "string",
            "sort": 99,
            "info": "邮箱服务器smtp",
            "value": "smtp.mxhichina.com"
        },
        "MAIL_SUBJECT_SUFFIX": {
            "type": "string",
            "sort": 99,
            "info": "发送邮件的标题后缀",
            "value": "OSROOM"
        },
        "APP_NAME": {
            "type": "string",
            "sort": 99,
            "info": "在邮件中显示的APP(WEB)名称(1.不填写则不显示.2.如果主题邮件发送html模板不支持，也不显示)",
            "value": ""
        },
        "__restart__": "must",
        "MAIL_PASSWORD": {
            "type": "password",
            "sort": 99,
            "info": "邮箱密码, 是用于发送邮件的密码",
            "value": "<Your password>"
        },
        "MAIL_USE_SSL": {
            "type": "bool",
            "sort": 99,
            "info": "是否使用SSL",
            "value": True
        },
        "MAIL_ASCII_ATTACHMENTS": {
            "type": "bool",
            "sort": 99,
            "info": "MAIL ASCII ATTACHMENTS",
            "value": True
        },
        "MAIL_PORT": {
            "type": "int",
            "sort": 99,
            "info": "邮箱服务器端口",
            "value": 465
        },
        "MAIL_FOOTER": {
            "type": "string",
            "sort": 99,
            "info": "发送邮件的页尾",
            "value": "OSROOM开源网站系统"
        },
        "MAIL_DEFAULT_SENDER": {
            "type": "list",
            "sort": 99,
            "info": "默认发送者邮箱　(显示名称, 邮箱地址)顺序不能调换",
            "value": [
                "OSR DEMO",
                "system@osroom.com"
            ]
        },
        "__sort__": 10,
        "__info__": "邮件发送参数设置（建议技术管理人员使用）"
    },
    "babel": {
        "__restart__": "must",
        "LANGUAGES": {
            "type": "dict",
            "sort": 99,
            "info": "管理端支持的语言",
            "value": {
                "zh_CN": {
                    "alias": "中文",
                    "name": "中文"
                },
                "en_US": {
                    "alias": "En",
                    "name": "English"
                }
            }
        },
        "__sort__": 9,
        "__info__": "多语言设置",
        "BABEL_DEFAULT_LOCALE": {
            "type": "string",
            "sort": 99,
            "info": "默认语言:可以是zh_CN, en_US等()",
            "value": "zh_CN"
        }
    },
    "cache": {
        "CACHE_TYPE": {
            "type": "string",
            "sort": 99,
            "info": "缓存使用的类型,可选择redis,mongodb",
            "value": "redis"
        },
        "CACHE_KEY_PREFIX": {
            "type": "string",
            "sort": 99,
            "info": "所有键(key)之前添加的前缀,这使得它可以为不同的应用程序使用相同的memcached(内存)服务器.",
            "value": "osr_cache"
        },
        "CACHE_DEFAULT_TIMEOUT": {
            "type": "int",
            "sort": 99,
            "info": "(s秒)默认缓存时间,当单个缓存没有设定缓存时间时会使用该时间",
            "value": 600
        },
        "__info__": "Web缓存参数设置（建议技术管理人员使用）",
        "__restart__": "must",
        "USE_CACHE": {
            "type": "bool",
            "sort": 99,
            "info": "是否使用缓存功能,建议开启",
            "value": True
        },
        "__sort__": 99,
        "CACHE_MONGODB_COLLECT": {
            "type": "string",
            "sort": 99,
            "info": "保存cache的collection,当CACHE_TYPE为mongodb时有效",
            "value": "osr_cache"
        }
    },
    "seo": {
        "__restart__": "not_must",
        "DEFAULT_DESCRIPTION": {
            "type": "string",
            "sort": 99,
            "info": "网站的页面默认简单描述",
            "value": "开源Web系统, 可以作为企业网站, 个人博客网站, 微信小程序Web服务端"
        },
        "__sort__": 4,
        "__info__": "针对网页客户端的简单的SEO配置<br>此模块所有的KEY值, 都可以直接请求全局Api(<br><span style='color:red;'>/api/global</span>)获取.<br>也可以直接在主题中使用Jinjia2模板引擎获取(<br><span style='color:red;'>g.site_global.site_config.XXXX</span>)",
        "DEFAULT_KEYWORDS": {
            "type": "string",
            "sort": 99,
            "info": "网站的页面默认关键词",
            "value": "开源, 企业网站, 博客网站, 微信小程序, Web服务端"
        }
    },
    "weblogger": {
        "__restart__": "not_must",
        "USER_OP_LOG_KEEP_NUM": {
            "type": "int",
            "sort": 99,
            "info": "用户操作日志保留个数",
            "value": 30
        },
        "__sort__": 99,
        "__info__": "操作日志设置",
        "SING_IN_LOG_KEEP_NUM": {
            "type": "int",
            "sort": 99,
            "info": "登录日志保留个数",
            "value": 30
        }
    },
    "upload": {
        "SAVE_DIR": {
            "type": "string",
            "sort": 99,
            "info": "上传:保存目录,如何存在'/'则会自动切分创建子目录",
            "value": "media"
        },
        "__info__": "文件上传配置（建议技术管理人员使用）",
        "UP_ALLOWED_EXTENSIONS": {
            "type": "list",
            "sort": 99,
            "info": "上传:允许上传的文件后缀(全部小写),每个用英文的','隔开",
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
            ]
        },
        "__restart__": "not_must",
        "IMG_VER_CODE_DIR": {
            "type": "string",
            "sort": 99,
            "info": "系统生成的图片验证码保存目录",
            "value": "verifi_code"
        },
        "__sort__": 99
    },
    "site_config": {
        "STATIC_FILE_VERSION": {
            "type": "int",
            "sort": 12,
            "info": "静态文件版本(当修改了CSS,JS等静态文件的时候，修改此版本号)",
            "value": 20180512080336
        },
        "TITLE_PREFIX_ADM": {
            "type": "string",
            "sort": 7,
            "info": "APP(Web)管理端Title前缀",
            "value": ""
        },
        "APP_NAME": {
            "type": "string",
            "sort": 1,
            "info": "APP(站点)名称,将作为全局变量使用在平台上",
            "value": "OSR DEMO"
        },
        "__info__": "基础设置: APP(Web)全局数据设置<br>此模块所有的KEY值, 都可以直接请求全局Api(/api/global)获取.也可以直接在主题中使用Jinjia2模板引擎获取(g.site_global.site_config.XXXX)",
        "PC_LOGO_DISPLAY": {
            "type": "string",
            "sort": 3,
            "info": "PC端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则显示Logo和App name<br>可填logo或name(需要主题支持)",
            "value": "logo"
        },
        "TITLE_SUFFIX": {
            "type": "string",
            "sort": 8,
            "info": "APP(Web)Title后缀",
            "value": "OSROOM开源Web DEMO"
        },
        "LOGO_IMG_URL": {
            "type": "string",
            "sort": 2,
            "info": "APP(Web)Logo的URL",
            "value": "/static/sys_imgs/osroom-logo.png"
        },
        "MB_LOGO_DISPLAY": {
            "type": "string",
            "sort": 4,
            "info": "移动端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则App name优先<br>可填logo或name(需要主题支持)",
            "value": "logo"
        },
        "SITE_URL": {
            "type": "string",
            "sort": 11,
            "info": "Web站点URL(如果没有填写, 则使用默认的当前域名首页地址)",
            "value": "http://www.osroom.com"
        },
        "HEAD_CODE": {
            "type": "string",
            "sort": 13,
            "info": "用于放入html中哦你<br><span style='color:red;'>head标签</span>内的js/css/html代码(如Google分析代码/百度统计代码)",
            "value": ""
        },
        "__sort__": 1,
        "LOGO_IMG_URL_SECONDAEY": {
            "type": "string",
            "sort": 5,
            "info": "APP(Web)Logo URL备用(需要主题支持)",
            "value": "/static/sys_imgs/osroom-logo-2.png"
        },
        "FRIEND_LINK": {
            "type": "dict",
            "sort": 11,
            "info": "友情链接:值(Value)格式为{'url':'友情链接', 'logo_url':'logo链接'}",
            "value": {
                "Github": {
                    "url": "https://github.com/osroom/osroom",
                    "logo_url": "http://osr.local.com:5000/static/admin/sys_imgs/osroom-logo-1.png?w=240&h=240"
                }
            }
        },
        "__restart__": "not_must",
        "TITLE_PREFIX": {
            "type": "string",
            "sort": 6,
            "info": "APP(Web)Title前缀",
            "value": ""
        },
        "TITLE_SUFFIX_ADM": {
            "type": "string",
            "sort": 9,
            "info": "APP(Web)管理端Title后缀",
            "value": "OSROOM管理端"
        },
        "FAVICON": {
            "type": "string",
            "sort": 10,
            "info": "APP(Web)favicon图标的URL",
            "value": "/static/sys_imgs/osroom-logo.ico"
        }
    }
}