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
        "SAVE_DIR": {
            "sort": 99,
            "type": "string",
            "info": "上传:保存目录,如何存在'/'则会自动切分创建子目录",
            "value": "media"
        },
        "UP_ALLOWED_EXTENSIONS": {
            "sort": 99,
            "type": "list",
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
        "__info__": "文件上传配置（建议技术管理人员使用）",
        "IMG_VER_CODE_DIR": {
            "sort": 99,
            "type": "string",
            "info": "系统生成的图片验证码保存目录",
            "value": "verifi_code"
        },
        "__sort__": 99
    },
    "comment": {
        "OPEN_COMMENT": {
            "sort": 99,
            "type": "bool",
            "info": "评论开关,是否打开评论功能?",
            "value": True
        },
        "NUM_PAGE_MAX": {
            "sort": 99,
            "type": "int",
            "info": "每个页面最多获取几条评论(此配置对管理端无效)",
            "value": 30
        },
        "NUM_OF_INTERVAL": {
            "sort": 99,
            "type": "int",
            "info": "控制评论频繁度时间内最多评论几次",
            "value": 3
        },
        "__info__": "评论内容设置",
        "MAX_LEN": {
            "sort": 99,
            "type": "int",
            "info": "发布评论最多几个字符",
            "value": 300
        },
        "__restart__": "not_must",
        "TRAVELER_COMMENT": {
            "sort": 99,
            "type": "bool",
            "info": "游客评论开关,是否打开?",
            "value": False
        },
        "NUM_PAGE": {
            "sort": 99,
            "type": "int",
            "info": "每个页面获取几条评论, 如果请求获取评论时指定了指定了per参数, 则此配置无效(此配置也对管理端无效)",
            "value": 10
        },
        "__sort__": 3,
        "INTERVAL": {
            "sort": 99,
            "type": "int",
            "info": "控制评论频繁度时间(s)",
            "value": 30
        }
    },
    "theme": {
        "CURRENT_THEME_NAME": {
            "sort": 99,
            "type": "string",
            "info": "当前主题名称,需与主题主目录名称相同",
            "value": "osr-style"
        }
    },
    "rest_auth_token": {
        "MAX_SAME_TIME_LOGIN": {
            "sort": 99,
            "type": "int",
            "info": "最多能同时登录几个使用JWT验证的客户端,超过此数目则会把旧的登录注销",
            "value": 3
        },
        "__restart__": "not_must",
        "REST_ACCESS_TOKEN_LIFETIME": {
            "sort": 99,
            "type": "int",
            "info": "给客户端发补的访问Token AccessToken的有效期",
            "value": 172800
        },
        "LOGIN_LIFETIME": {
            "sort": 99,
            "type": "int",
            "info": "jwt 登录BearerToken有效期(s)",
            "value": 2592000
        },
        "__info__": "Web参数设置",
        "__sort__": 99
    },
    "permission": {
        "SYS_SETTING": {
            "sort": 99,
            "type": "int",
            "info": "17b|网站系统设置",
            "value": 65536
        },
        "__info__": "权限设置[root用户才有权修改](建议技术管理人员使用）",
        "FINANCE": {
            "sort": 99,
            "type": "int",
            "info": "14b|财务, 涉及资金转账之类",
            "value": 8192
        },
        "ROOT": {
            "sort": 99,
            "type": "int",
            "info": "32b|超级管理, 有权控制ADMIN和IMPORTANT_DATA_DEL分配",
            "value": 2147483648
        },
        "USER_MANAGE": {
            "sort": 99,
            "type": "int",
            "info": "12b|用户类管理,包括Role, User",
            "value": 2048
        },
        "STAFF": {
            "sort": 99,
            "type": "int",
            "info": "8b|拥有此权重的用户被视为工作人员, 用法:如果比如一个需要SYS_SETTING权限才能查看的数据, 你可以自定义权限让STAFF可以使用GET请求方式(只开放查看)",
            "value": 128
        },
        "ORDER": {
            "sort": 99,
            "type": "int",
            "info": "13b|订单管理权限",
            "value": 4096
        },
        "REPORT": {
            "sort": 99,
            "type": "int",
            "info": "9b|报表查看权限",
            "value": 256
        },
        "EDITOR": {
            "sort": 99,
            "type": "int",
            "info": "10b|管理端文字,图片编辑权重",
            "value": 512
        },
        "WEB_SETTING": {
            "sort": 99,
            "type": "int",
            "info": "16b|网站基础设置",
            "value": 32768
        },
        "ADMIN": {
            "sort": 99,
            "type": "int",
            "info": "28b|管理, 有权控制除ROOT,IMPORTANT_DATA_DEL外的其他角色分配",
            "value": 134217728
        },
        "__sort__": 99,
        "IMPORTANT_DATA_DEL": {
            "sort": 99,
            "type": "int",
            "info": "30b|重要数据管理权限",
            "value": 536870912
        },
        "__restart__": "not_must",
        "DATA_MANAGE": {
            "sort": 99,
            "type": "int",
            "info": "15b|网站数据管理, 涉及数据备份等",
            "value": 16384
        },
        "USER": {
            "sort": 99,
            "type": "int",
            "info": "1b|普通用户权重",
            "value": 1
        },
        "AUDIT": {
            "sort": 99,
            "type": "int",
            "info": "11b|审核权限,主页针对普通用户发布的内容进行审核",
            "value": 1024
        }
    },
    "content_inspection": {
        "IMAGE_OPEN": {
            "sort": 99,
            "type": "bool",
            "info": "开启图片检测.需要hook_name为content_inspection_image的图片检测插件",
            "value": False
        },
        "__info__": "内容检查配置(需要安装相关插件该配置才生效).<br>检测开关:<br>1.如果开启, 并安装有相关的自动检查插件, 则会给发布的内容给出违规评分.如果未安装自动审核插件,则系统会给予评分100分(属涉嫌违规,网站工作人员账户除外).<br>2.如果关闭审核，则系统会给评分0分(不违规)",
        "__restart__": "not_must",
        "ALLEGED_ILLEGAL_SCORE": {
            "sort": 99,
            "type": "float",
            "info": "内容检测分数高于多少分时属于涉嫌违规(0-100分,对于需要检查的内容有效)",
            "value": 99
        },
        "AUDIO_OPEN": {
            "sort": 99,
            "type": "bool",
            "info": "开启音频检测.需要hook_name为content_inspection_audio的音频检测插件",
            "value": False
        },
        "VEDIO_OPEN": {
            "sort": 99,
            "type": "bool",
            "info": "开启视频检测.需要hook_name为content_inspection_vedio的视频检测插件",
            "value": False
        },
        "__sort__": 5,
        "TEXT_OPEN": {
            "sort": 99,
            "type": "bool",
            "info": "开启text检测.需要hook_name为content_inspection_text的文本检测插件",
            "value": True
        }
    },
    "email": {
        "MAIL_ASCII_ATTACHMENTS": {
            "sort": 99,
            "type": "bool",
            "info": "MAIL ASCII ATTACHMENTS",
            "value": True
        },
        "__info__": "邮件发送参数设置（建议技术管理人员使用）",
        "MAIL_SERVER": {
            "sort": 99,
            "type": "string",
            "info": "邮箱服务器smtp",
            "value": "smtp.mxhichina.com"
        },
        "MAIL_SUBJECT_SUFFIX": {
            "sort": 99,
            "type": "string",
            "info": "发送邮件的标题后缀",
            "value": "OSROOM"
        },
        "MAIL_FOOTER": {
            "sort": 99,
            "type": "string",
            "info": "发送邮件的页尾",
            "value": "OSROOM开源网站系统www.osroom.com"
        },
        "__sort__": 10,
        "MAIL_USERNAME": {
            "sort": 99,
            "type": "string",
            "info": "邮箱用户名",
            "value": "system@osroom.com"
        },
        "MAIL_PORT": {
            "sort": 99,
            "type": "int",
            "info": "邮箱服务器端口",
            "value": 465
        },
        "__restart__": "must",
        "APP_LOG_URL": {
            "sort": 99,
            "type": "string",
            "info": "在邮件中显示的LOGO图片URL(1.不填写则不显示.2.如果主题邮件发送html模板不支持，也不显示)",
            "value": "https://osroom-test2.oss-cn-shenzhen.aliyuncs.com/multimedia/image/a82d6b56-3fa9-11e8-bff8-001c42462937.png"
        },
        "MAIL_DEFAULT_SENDER": {
            "sort": 99,
            "type": "list",
            "info": "默认发送者邮箱　(显示名称, 邮箱地址)顺序不能调换",
            "value": [
                "OSR DEMO",
                "system@osroom.com"
            ]
        },
        "MAIL_USE_TLS": {
            "sort": 99,
            "type": "bool",
            "info": "是否使用TLS",
            "value": False
        },
        "APP_NAME": {
            "sort": 99,
            "type": "string",
            "info": "在邮件中显示的APP(WEB)名称(1.不填写则不显示.2.如果主题邮件发送html模板不支持，也不显示)",
            "value": ""
        },
        "MAIL_USE_SSL": {
            "sort": 99,
            "type": "bool",
            "info": "是否使用SSL",
            "value": True
        },
        "MAIL_PASSWORD": {
            "sort": 99,
            "type": "password",
            "info": "邮箱密码, 是用于发送邮件的密码",
            "value": "<Your password>"
        }
    },
    "user_model": {
        "__restart__": "not_must",
        "__info__": "用户Model",
        "__sort__": 99,
        "EDITOR": {
            "sort": 99,
            "type": "string",
            "info": "新用户默认编辑器类型rich_text或markdown",
            "value": "rich_text"
        }
    },
    "seo": {
        "__info__": "简单的SEO配置<br>此模块所有的KEY值, 都可以直接请求全局Api(/api/global)获取,也可以直接在主题中使用Jinjia2模板引擎获取(g.site_global.site_config.XXXX)",
        "DEFAULT_KEYWORDS": {
            "sort": 99,
            "type": "string",
            "info": "网站的页面默认关键词",
            "value": "开源, 企业网站, 博客网站, 微信小程序, Web服务端"
        },
        "__restart__": "not_must",
        "DEFAULT_DESCRIPTION": {
            "sort": 99,
            "type": "string",
            "info": "网站的页面默认简单描述",
            "value": "开源Web系统, 可以作为企业网站, 个人博客网站, 微信小程序Web服务端"
        },
        "__sort__": 4
    },
    "account": {
        "__restart__": "not_must",
        "DEFAULT_AVATAR": {
            "sort": 99,
            "type": "string",
            "info": "新注册用户默认头像的URL",
            "value": "/static/sys_imgs/avatar_default.png"
        },
        "USER_AVATAR_SIZE": {
            "sort": 99,
            "type": "list",
            "info": "用户头像保存大小[<width>, <height>]像素",
            "value": [
                "360",
                "360"
            ]
        },
        "__info__": "账户设置",
        "USER_AVATAR_MAX_SIZE": {
            "sort": 99,
            "type": "float",
            "info": "用户头像不能上传超过此值大小(单位Mb)的图片作头像",
            "value": 0.0001
        },
        "USERNAME_MAX_LEN": {
            "sort": 99,
            "type": "int",
            "info": "用户名最大长度",
            "value": 20
        },
        "__sort__": 6
    },
    "system": {
        "MAX_CONTENT_LENGTH": {
            "sort": 1,
            "type": "float",
            "info": "拒绝内容长度大于此值的请求进入，并返回一个 413 状态码(单位:Mb)",
            "value": 50.0
        },
        "__restart__": "must",
        "__info__": "其他web系统参数设置（建议技术管理人员使用）",
        "TEMPLATES_AUTO_RELOAD": {
            "sort": 99,
            "type": "bool",
            "info": "是否自动加载页面(html)模板.开启后,每次html页面修改都无需重启Web",
            "value": True
        },
        "__sort__": 99
    },
    "key": {
        "__restart__": "must",
        "SECRET_KEY": {
            "sort": 99,
            "type": "string",
            "info": "安全验证码",
            "value": "12333r32fddvve"
        },
        "__info__": "安全Key（建议技术管理人员使用）",
        "__sort__": 99,
        "SECURITY_PASSWORD_SALT": {
            "sort": 99,
            "type": "string",
            "info": "安全密码码盐值",
            "value": "12343erfegrg"
        }
    },
    "name_audit": {
        "AUDIT_PROJECT_KEY": {
            "sort": 99,
            "type": "dict",
            "info": "审核项目的Key(键),审核时会使用一个Key来获取审核规则,正则去匹配用户输入的内容",
            "value": {
                "username": "审核用户名",
                "class_name": "审核一些短的分类名称, 如category, tag"
            }
        },
        "__info__": "名称验证, 如用户名,分类名称",
        "__restart__": "not_must",
        "__sort__": 8
    },
    "category": {
        "__info__": "Web参数设置",
        "CATEGORY_MAX_LEN": {
            "sort": 99,
            "type": "int",
            "info": "分类名称类型名最多几个字符",
            "value": 30
        },
        "__restart__": "not_must",
        "CATEGORY_TYPE": {
            "sort": 99,
            "type": "dict",
            "info": "分类的品种只能有这几种",
            "value": {
                "其他类型库": "other",
                "文本内容": "text",
                "视频库": "video",
                "图文|图库": "image",
                "文集": "post",
                "音频库": "audio"
            }
        },
        "__sort__": 7
    },
    "babel": {
        "LANGUAGES": {
            "sort": 99,
            "type": "dict",
            "info": "管理端支持的语言",
            "value": {
                "en_US": {
                    "alias": "En",
                    "name": "English"
                },
                "zh_CN": {
                    "alias": "中文",
                    "name": "中文"
                }
            }
        },
        "BABEL_DEFAULT_LOCALE": {
            "sort": 99,
            "type": "string",
            "info": "默认语言:可以是zh_CN, en_US等()",
            "value": "zh_CN"
        },
        "__restart__": "must",
        "__info__": "多语言设置",
        "__sort__": 9
    },
    "cache": {
        "__info__": "Web缓存参数设置（建议技术管理人员使用）",
        "CACHE_TYPE": {
            "sort": 99,
            "type": "string",
            "info": "缓存使用的类型,可选择redis,mongodb",
            "value": "redis"
        },
        "__restart__": "must",
        "USE_CACHE": {
            "sort": 99,
            "type": "bool",
            "info": "是否使用缓存功能,建议开启",
            "value": True
        },
        "CACHE_KEY_PREFIX": {
            "sort": 99,
            "type": "string",
            "info": "所有键(key)之前添加的前缀,这使得它可以为不同的应用程序使用相同的memcached(内存)服务器.",
            "value": "osr_cache"
        },
        "CACHE_MONGODB_COLLECT": {
            "sort": 99,
            "type": "string",
            "info": "保存cache的collection,当CACHE_TYPE为mongodb时有效",
            "value": "osr_cache"
        },
        "__sort__": 99,
        "CACHE_DEFAULT_TIMEOUT": {
            "sort": 99,
            "type": "int",
            "info": "(s秒)默认缓存时间,当单个缓存没有设定缓存时间时会使用该时间",
            "value": 600
        }
    },
    "verify_code": {
        "MAX_NUM_SEND_SAMEIP_PERMIN_NO_IMGCODE": {
            "sort": 99,
            "type": "int",
            "info": "同一IP地址,同一用户(未登录的同属同一匿名用户),允许每分钟在不验证[图片验证码]的时候,调用API发送验证码最大次数.超过次数后API会生成[图片验证码]并返回图片url对象(也可以自己调用获取图片验证码API获取).如果你的客户端(包括主题)不支持显示图片验证码,请设置此配置为99999999",
            "value": 1
        },
        "SEND_CODE_TYPE": {
            "sort": 99,
            "type": "dict",
            "info": "发送的验证码字符类型，与字符个数",
            "value": {
                "int": 6,
                "string": 0
            }
        },
        "IMG_CODE_DIR": {
            "sort": 99,
            "type": "string",
            "info": "图片验证码保存目录",
            "value": "admin/verify_code"
        },
        "__restart__": "not_must",
        "MAX_NUM_SEND_SAMEIP_PERMIN": {
            "sort": 99,
            "type": "int",
            "info": "同一IP地址,同一用户(未登录的同属一匿名用户), 允许每分钟调用API发送验证码的最大次数",
            "value": 15
        },
        "MAX_IMG_CODE_INTERFERENCE": {
            "sort": 99,
            "type": "int",
            "info": "图片验证码干扰程度的最大值",
            "value": 40
        },
        "__info__": "验证码(建议技术管理员配置)",
        "MIN_IMG_CODE_INTERFERENCE": {
            "sort": 99,
            "type": "int",
            "info": "图片验证码干扰程度的最小值,最小值小于10时无效",
            "value": 10
        },
        "EXPIRATION": {
            "sort": 99,
            "type": "int",
            "info": "验证码过期时间(s)",
            "value": 600
        },
        "__sort__": 11
    },
    "site_config": {
        "SITE_URL": {
            "sort": 11,
            "type": "string",
            "info": "Web站点URL(如果没有填写, 则使用默认的当前域名首页地址)",
            "value": "http://www.osroom.com"
        },
        "MB_LOGO_DISPLAY": {
            "sort": 4,
            "type": "string",
            "info": "移动端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则App name优先<br>可填logo或name(需要主题支持)",
            "value": "logo"
        },
        "TITLE_SUFFIX_ADM": {
            "sort": 9,
            "type": "string",
            "info": "APP(Web)管理端Title后缀",
            "value": "OSROOM管理端"
        },
        "__info__": "基础设置: APP(Web)全局数据设置<br>此模块所有的KEY值, 都可以直接请求全局Api(/api/global)获取,也可以直接在主题中使用Jinjia2模板引擎获取(g.site_global.site_config.XXXX)",
        "FRIEND_LINK": {
            "sort": 11,
            "type": "dict",
            "info": "友情链接:值(Value)格式为{'url':'友情链接', 'logo_url':'logo链接'}",
            "value": {
                "Github": {
                    "url": "https://github.com/osroom/osroom",
                    "logo_url": "http://osr.local.com:5000/static/admin/sys_imgs/osroom-logo-1.png?w=240&h=240"
                }
            }
        },
        "TITLE_PREFIX_ADM": {
            "sort": 7,
            "type": "string",
            "info": "APP(Web)管理端Title前缀",
            "value": ""
        },
        "FAVICON": {
            "sort": 10,
            "type": "string",
            "info": "APP(Web)favicon图标的URL",
            "value": "https://osroom-test2.oss-cn-shenzhen.aliyuncs.com/multimedia/image/0220d5b6-4321-11e8-bff8-001c42462937.ico"
        },
        "TITLE_SUFFIX": {
            "sort": 8,
            "type": "string",
            "info": "APP(Web)Title后缀",
            "value": "OSROOM开源Web DEMO"
        },
        "LOGO_IMG_URL": {
            "sort": 2,
            "type": "string",
            "info": "APP(Web)Logo的URL",
            "value": "/static/sys_imgs/osroom-logo.png"
        },
        "PC_LOGO_DISPLAY": {
            "sort": 3,
            "type": "string",
            "info": "PC端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则显示Logo和App name<br>可填logo或name(需要主题支持)",
            "value": "logo"
        },
        "LOGO_IMG_URL_SECONDAEY": {
            "sort": 5,
            "type": "string",
            "info": "APP(Web)Logo URL备用(需要主题支持)",
            "value": "/static/sys_imgs/osroom-logo-2.png"
        },
        "TITLE_PREFIX": {
            "sort": 6,
            "type": "string",
            "info": "APP(Web)Title前缀",
            "value": ""
        },
        "STATIC_FILE_VERSION": {
            "sort": 12,
            "type": "int",
            "info": "静态文件版本(当修改了CSS,JS等静态文件的时候，修改此版本号)",
            "value": 20180512080336
        },
        "HEAD_CODE": {
            "sort": 13,
            "type": "string",
            "info": "用于放入html中哦你head标签内的js/css/html代码(如Google分析代码/百度统计代码)",
            "value": ""
        },
        "__restart__": "not_must",
        "APP_NAME": {
            "sort": 1,
            "type": "string",
            "info": "APP(站点)名称,将作为全局变量使用在平台上",
            "value": "OSR DEMO"
        },
        "__sort__": 1
    },
    "session": {
        "PERMANENT_SESSION_LIFETIME": {
            "sort": 99,
            "type": "int",
            "info": "永久会话的有效期.",
            "value": 2592000
        },
        "__info__": "Session参数设置（建议技术管理人员使用）",
        "SESSION_MONGODB_COLLECT": {
            "sort": 99,
            "type": "string",
            "info": "Mongodb保存session的collection,当SESSION_TYPE为mongodb时有效",
            "value": "osr_session"
        },
        "SESSION_PERMANENT": {
            "sort": 99,
            "type": "bool",
            "info": "是否使用永久会话",
            "value": True
        },
        "SESSION_TYPE": {
            "sort": 99,
            "type": "string",
            "info": "保存Session会话的类型,可选mongodb, redis",
            "value": "redis"
        },
        "__restart__": "must",
        "SESSION_KEY_PREFIX": {
            "sort": 99,
            "type": "string",
            "info": "添加一个前缀,之前所有的会话密钥。这使得它可以为不同的应用程序使用相同的后端存储服务器",
            "value": "osr-session:"
        },
        "__sort__": 99
    },
    "login_manager": {
        "LOGIN_OUT_TO": {
            "sort": 99,
            "type": "string",
            "info": "退出登录后,api会响应数据会带上需要跳转到路由to_url:<LOGIN_OUT_TO>",
            "value": "/"
        },
        "PW_WRONG_NUM_IMG_CODE": {
            "sort": 99,
            "type": "int",
            "info": "同一用户登录密码错误几次后响应图片验证码, 并且需要验证",
            "value": 5
        },
        "OPEN_REGISTER": {
            "sort": 99,
            "type": "bool",
            "info": "开放注册",
            "value": True
        },
        "LOGIN_IN_TO": {
            "sort": 99,
            "type": "string",
            "info": "登录成功后,api会响应数据会带上需要跳转到路由to_url:<LOGIN_IN_TO>",
            "value": "/"
        },
        "__restart__": "not_must",
        "__info__": "在线管理（建议技术管理人员使用）",
        "LOGIN_VIEW": {
            "sort": 99,
            "type": "string",
            "info": "需要登录的页面,未登录时,api会响应401,并带上需要跳转到路由to_url:<LOGIN_VIEW>",
            "value": "/sign-in"
        },
        "__sort__": 99
    },
    "post": {
        "BRIEF_LEN": {
            "sort": 99,
            "type": "int",
            "info": "获取文章简要的字数",
            "value": 80
        },
        "__restart__": "not_must",
        "__sort__": 2,
        "MAX_LEN": {
            "sort": 99,
            "type": "int",
            "info": "发布文章最多几个字符",
            "value": 5000
        },
        "NUM_PAGE_MAX": {
            "sort": 99,
            "type": "int",
            "info": "每个页面最多获取几篇文章(此配置对管理端无效)",
            "value": 30
        },
        "TAG_MAX_NUM": {
            "sort": 99,
            "type": "int",
            "info": "POST标签最大个数",
            "value": 5
        },
        "NUM_PAGE": {
            "sort": 99,
            "type": "int",
            "info": "每个页面获取几篇文章, 如果请求获取文章时指定了指定了per参数, 则此配置无效(此配置也对管理端无效)",
            "value": 15
        },
        "TAG_MAX_LEN": {
            "sort": 99,
            "type": "int",
            "info": "POST标签最多几个字",
            "value": 10
        },
        "TITLE_MAX_LEN": {
            "sort": 99,
            "type": "int",
            "info": "文章Title最大长度",
            "value": 50
        },
        "__info__": "文章内容设置"
    },
    "weblogger": {
        "__restart__": "not_must",
        "SING_IN_LOG_KEEP_NUM": {
            "sort": 99,
            "type": "int",
            "info": "登录日志保留个数",
            "value": 30
        },
        "__info__": "操作日志设置",
        "__sort__": 99,
        "USER_OP_LOG_KEEP_NUM": {
            "sort": 99,
            "type": "int",
            "info": "用户操作日志保留个数",
            "value": 30
        }
    },
    "py_venv": {
        "VENV_PATH": {
            "sort": 99,
            "type": "string",
            "info": "\"python\"虚拟环境路径",
            "value": "/home/work/project/venv3"
        }
    }
}