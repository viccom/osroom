# -*-coding:utf-8-*-
__author__ = "Allen Woo"
DB_CONFIG = {
    "mongodb": {
        "mongo_sys": {
            "host": [
                "127.0.0.1:27017"
            ],
            "dbname": "osr_sys",
            "password": "<Your password>",
            "config": {
                "replica_set": None,
                "fsync": False
            },
            "username": "work"
        },
        "mongo_user": {
            "host": [
                "127.0.0.1:27017"
            ],
            "dbname": "osr_user",
            "password": "<Your password>",
            "config": {
                "replica_set": None,
                "fsync": False
            },
            "username": "work"
        },
        "mongo_web": {
            "host": [
                "127.0.0.1:27017"
            ],
            "dbname": "osr_web",
            "password": "<Your password>",
            "config": {
                "replica_set": None,
                "fsync": False
            },
            "username": "work"
        }
    },
    "redis": {
        "port": [
            "6379"
        ],
        "host": [
            "127.0.0.1"
        ],
        "password": "<Your password>"
    }
}