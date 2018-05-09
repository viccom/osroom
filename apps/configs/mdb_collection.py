# -*-coding:utf-8-*-
__author__ = 'Allen Woo'

collections = {"mdb_web":[
                        "post",         # 发布的文章内容
                        "comment",      # 评论
                        "category",     # 分类集合
                        "access_record", # 访问记录
                        "verify_code",    # web验证码
                        "tempfile",     # 用于保存临时文件
                        "media",        # 用于保存媒体的信息,如图片
                            ],
            "mdb_sys":[
                        'sys_token',
                        'audit_rules',
                        'sys_message',
                        'sys_config',
                        'sys_host',
                        'sys_call_record',# 用户一些操作频率记录
                        'plugin',
                        'plugin_config',
                        'theme'
                ],
            "mdb_user":[
                        "role",         # 用户角色
                        "user",         # 用户
                        "user_login_log",# 用户登录日志
                        "user_op_log",  # 用户操作日志
                        "user_like",  # 用户点赞的内容
                        "message",   # 用户消息
                        "user_follow" # 用户关注
                        ]
            }
