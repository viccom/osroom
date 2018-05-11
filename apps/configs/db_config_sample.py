# -*-coding:utf-8-*-
__author__ = "Allen Woo"
DB_CONFIG = {
    "redis": {
        "port": [
            "6379"
        ],
        "password": "<Your password>",
        "host": [
            "127.0.0.1"
        ]
    },
    "mongodb": {
        "mongo_sys": {
            "password": "<Your password>",
            "config": {
                "replica_set": None,
                "fsync": False
            },
            "dbname": "osr_sys",
            "username": "work",
            "host": [
                "127.0.0.1:27017"
            ]
        },
        "mongo_web": {
            "password": "<Your password>",
            "config": {
                "replica_set": None,
                "fsync": False
            },
            "dbname": "osr_web",
            "username": "work",
            "host": [
                "127.0.0.1:27017"
            ]
        },
        "mongo_user": {
            "password": "<Your password>",
            "config": {
                "replica_set": None,
                "fsync": False
            },
            "dbname": "osr_user",
            "username": "work",
            "host": [
                "127.0.0.1:27017"
            ]
        }
    }
}