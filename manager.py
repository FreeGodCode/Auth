import os

from flask import Flask, render_template, g

# app = Flask(__name__)
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.models.Organization import Organization
from app.models.Resource import Resource
from app.models.ResourceType import ResourceType
from app.models.Role import Role
from app.models.User import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

with app.app_context():
    g. contextPath = ''


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Resource=Resource, ResourceType=ResourceType, Organization=Organization)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@app.errorhandler(404)
def page_not_found(e):
    """
    页面没有找到报404错误
    :param e:
    :return:
    """
    return render_template('errors/404.html'), 404


# @app.route('/')
# def hello_world():
#     return 'Hello World!'
@manager.command
def myprint():
    print('hello world!')


if __name__ == '__main__':
    manager.run()
