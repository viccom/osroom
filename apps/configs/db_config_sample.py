# -*-coding:utf-8-*-
__author__ = "Allen Woo"
DB_CONFIG = {
    "mongodb": {
        "mongo_user": {
            "dbname": "osr_user",
            "username": "work",
            "password": "<Your password>",
            "host": [
                "127.0.0.1:27017"
            ],
            "config": {
                "replica_set": None,
                "fsync": False
            }
        },
        "mongo_web": {
            "dbname": "osr_web",
            "username": "work",
            "password": "<Your password>",
            "host": [
                "127.0.0.1:27017"
            ],
            "config": {
                "replica_set": None,
                "fsync": False
            }
        },
        "mongo_sys": {
            "dbname": "osr_sys",
            "username": "work",
            "password": "<Your password>",
            "host": [
                "127.0.0.1:27017"
            ],
            "config": {
                "replica_set": None,
                "fsync": False
            }
        }
    },
    "redis": {
        "port": [
            "6379"
        ],
        "password": "<Your password>",
        "host": [
            "127.0.0.1"
        ]
    }
}