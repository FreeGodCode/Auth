# -*- coding: utf-8  -*-
# @Author: ty
# @File name: __init__.py 
# @IDE: PyCharm
# @Create time: 12/19/20 4:55 PM
from datetime import datetime

from flask_login import UserMixin

from app import db

# 用户组织关联表
user_organization_table = db.Table(
    'db_user_organization',
    db.Model.metadata,
    db.Column('user_id', db.String, db.ForeignKey('db_user.id')),
    db.Column('organization_id', db.String, db.ForeignKey('db_organization.id'))
)

# 用户角色关联表
user_role_table = db.Table(
    'db_user_role',
    db.Model.metadata,
    db.Column('user_id', db.String, db.ForeignKey('db_user.id')),
    db.Column('role_id', db.String, db.ForeignKey('db_role.id'))
)


class User(db.Model, UserMixin):
    """用户模型类"""
    __tablename__ = 'db_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, index=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(1))
    nickname = db.Column(db.String(100))
    password = db.Column(db.String(100))
    img = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True, default=datetime.now)
    employ_date = db.Column(db.DATETIME, default=datetime.now)

    organizations = db.relationship('Organization',
                                    secondary=user_organization_table,
                                    backref=db.backref('db_user', lazy='dynamic'),)

    roles = db.relationship('Role',
                            secondary=user_role_table,
                            backref=db.backref('db_user', lazy='dynamic'),)

    def get_id(self):
        return str(self.id)

    def have_permission(self, url):
        permissions = []
        for role in self.roles:
            permissions.extend([resource for resource in role.resources])

        if filter(lambda x: x.URL == url, permissions):
            return True

        permissions = []
        for organization in self.organizations:
            permissions.extend([resource for resource in organization.resources])

        return filter(lambda x: x.NAME == url, permissions)

    def __repr__(self):
        return '<User %s>\n' % (self.name)

    def to_join(self):
        return {
            'id': self.id,
            'create_datetime': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_datetime': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'nicknam': self.nickname,
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'img': self.img,
            'employdate': self.employ_date.strftime('%Y-%m-%d %H:%M:%S'),
        }


def load_user(user_id):
    """
    根据user_id查询
    :param user_id:
    :return:
    """
    return User.query.filter(User.id == user_id).first()


