# -*- coding: utf-8  -*-
# @Author: ty
# @File name: __init__.py 
# @IDE: PyCharm
# @Create time: 12/19/20 4:36 PM
from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

loginmanager = LoginManager()
loginmanager.session_protection = 'strong'
loginmanager.login_view = 'base.login'

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
base_blueprint = Blueprint('base', __name__, url_prefix='/base')


def create_app(config_name):
    # app = Flask(__file__)
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    loginmanager.init_app(app)

    app.register_blueprint(base_blueprint)

    return app




