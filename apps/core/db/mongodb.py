#-*-coding:utf-8-*-
from pymongo import MongoClient

__author__ = 'Allen Woo'


class PyMongo():

    '''
    mondodb 数据库链接初始化类
    '''

    def __init__(self, app=None, config_prefix='MONGO', db_config= None):
        if app or db_config:
            self.init_app(app, config_prefix, db_config)
        pass

    def init_app(self, app=None, config_prefix='MONGO', db_config= None, reinit=False):
        '''
        初始化数据库库连接模块
        :param app:
        :param config_prefix:
        :param db_config:
        :return:
        '''
        if not reinit:
            if not app and not db_config:
                raise Exception("Parameter: app or db_config must provide one")
            if app:
                def key(suffix):
                    return '%s_%s' % (config_prefix, suffix)
                if key('URI') in app.config:
                    # connection
                    self.config = app.config[key('URI')]
                else:
                    raise Exception("{} is not in the database configuration file".format(key('URI')))

            elif db_config:
                # connection
                self.config = db_config

        if self.config['replica_set']:
            self.connection = MongoClient(
                self.config['mongodb'],
                fsync=self.config['fsync'],
                read_preference = self.config['read_preference'],
                replicaSet = self.config['replica_set']
                )
        else:
            self.connection = MongoClient(
                self.config['mongodb'],
                fsync=self.config['fsync'],
                read_preference = self.config['read_preference'],
                )
        self.name = self.config['db']
        self.dbs = self.connection[self.config['db']]
        self.db = Conlections(self.dbs)


class Conlections():

    def __init__(self, conn_db = None):
        if conn_db:
            self.conlection_object(conn_db)

    def conlection_object(self, conn_db):

        for conlection in conn_db.collection_names():
            #print conlection
            self.__dict__[conlection] = conn_db[conlection]
