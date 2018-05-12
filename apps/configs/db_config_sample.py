# -*-coding:utf-8-*-
__author__ = "Allen Woo"
DB_CONFIG = {
    "redis": {
        "host": [
            "127.0.0.1"
        ],
        "password": "<Your password>",
        "port": [
            "6379"
        ]
    },
    "mongodb": {
        "mongo_web": {
            "username": "work",
            "host": [
                "127.0.0.1:27017"
            ],
            "password": "<Your password>",
            "dbname": "osr_web",
            "config": {
                "fsync": False,
                "replica_set": None
            }
        },
        "mongo_sys": {
            "username": "work",
            "host": [
                "127.0.0.1:27017"
            ],
            "password": "<Your password>",
            "dbname": "osr_sys",
            "config": {
                "fsync": False,
                "replica_set": None
            }
        },
        "mongo_user": {
            "username": "work",
            "host": [
                "127.0.0.1:27017"
            ],
            "password": "<Your password>",
            "dbname": "osr_user",
            "config": {
                "fsync": False,
                "replica_set": None
            }
        }
    }
}