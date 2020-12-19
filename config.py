# -*- coding: utf-8  -*-
# @Author: ty
# @File name: config.py
# @IDE: PyCharm
# @Create time: 12/19/20 4:02 PM
import os

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    """项目配置父类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tycarry'
    FLASK_MAIL_SUBJECT_PREFIX = 'Flask'
    FLASK_MAIL_SENDER = 'thechosenone_ty@163.com'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """ 开发环境配置"""
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USER_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/db_auth?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'mysql://root:123456@127.0.0.1:3306/db_auth?charset=utf8'


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///' + os.path.join(BASE_DIR, 'db_test.sqlite')


class ProductionConfig(Config):
    """生产环境配置"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(BASE_DIR, 'db_auth.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}