# -*-coding:utf-8-*-
__author__ = "Allen Woo"
DB_CONFIG = {
    "mongodb": {
        "mongo_sys": {
            "password": "<Your password>",
            "username": "work",
            "dbname": "osr_sys",
            "config": {
                "replica_set": None,
                "fsync": False
            },
            "host": [
                "127.0.0.1:27017"
            ]
        },
        "mongo_web": {
            "password": "<Your password>",
            "username": "work",
            "dbname": "osr_web",
            "config": {
                "replica_set": None,
                "fsync": False
            },
            "host": [
                "127.0.0.1:27017"
            ]
        },
        "mongo_user": {
            "password": "<Your password>",
            "username": "work",
            "dbname": "osr_user",
            "config": {
                "replica_set": None,
                "fsync": False
            },
            "host": [
                "127.0.0.1:27017"
            ]
        }
    },
    "redis": {
        "password": "<Your password>",
        "port": [
            "6379"
        ],
        "host": [
            "127.0.0.1"
        ]
    }
}