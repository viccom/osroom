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
            "dbname": "osr_web",
            "host": [
                "127.0.0.1:27017"
            ],
            "config": {
                "replica_set": None,
                "fsync": False
            }
        },
        "mongo_user": {
            "password": "<Your password>",
            "username": "work",
            "dbname": "osr_user",
            "host": [
                "127.0.0.1:27017"
            ],
            "config": {
                "replica_set": None,
                "fsync": False
            }
        },
        "mongo_sys": {
            "password": "<Your password>",
            "username": "work",
            "dbname": "osr_sys",
            "host": [
                "127.0.0.1:27017"
            ],
            "config": {
                "replica_set": None,
                "fsync": False
            }
        }
    }
}