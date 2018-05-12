# -*-coding:utf-8-*-
__author__ = "Allen Woo"
DB_CONFIG = {
    "redis": {
        "password": "<Your password>",
        "host": [
            "127.0.0.1"
        ],
        "port": [
            "6379"
        ]
    },
    "mongodb": {
        "mongo_web": {
            "password": "<Your password>",
            "username": "work",
            "config": {
                "fsync": False,
                "replica_set": None
            },
            "host": [
                "127.0.0.1:27017"
            ],
            "dbname": "osr_web"
        },
        "mongo_user": {
            "password": "<Your password>",
            "username": "work",
            "config": {
                "fsync": False,
                "replica_set": None
            },
            "host": [
                "127.0.0.1:27017"
            ],
            "dbname": "osr_user"
        },
        "mongo_sys": {
            "password": "<Your password>",
            "username": "work",
            "config": {
                "fsync": False,
                "replica_set": None
            },
            "host": [
                "127.0.0.1:27017"
            ],
            "dbname": "osr_sys"
        }
    }
}