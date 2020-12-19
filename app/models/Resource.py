# -*- coding: utf-8  -*-
# @Author: ty
# @File name: __init__.py 
# @IDE: PyCharm
# @Create time: 12/19/20 4:55 PM
from datetime import datetime

from flask_login import UserMixin

from app import db


class Resource(db.Model, UserMixin):
    """资源模型类"""
    __tablename__ = 'db_resource'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    url = db.Column(db.String(256))
    desc = db.Column(db.String(256))
    icons = db.Column(db.String(256))
    seq = db.Column(db.Integer)
    target = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True, default=datetime.now)

    resource_id = db.Column(db.String, db.ForeignKey('db_resource.id'))

    resource_type_id = db.Column(db.String, db.ForeignKey('db_resource_type.id'))

    parent = db.relationship('Resource', remote_side=[id], backref='resource', uselist=False)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Resource name: %s url: %s>\n' % (self.name, self.url)

    def get_pid(self):
        if self.parent:
            return self.parent.id
        return ''

    def get_type_json(self):
        if self.type:
            return self.type.to_join()
        return {}

    def to_join(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'desc': self.desc,
            'icons': self.icons,
            'seq': self.seq,
            'target': self.target,
            'create_time': self.create_time,
            'update_time': self.update_time,
            'pid': self.get_pid(),
            'resource_type': self.get_type_json()
        }

    def to_menu_json(self):
        return {
            'id': self.id,
            'icons': self.icons,
            'pid': self.get_pid(),
            'state': 'open',
            'checked': False,
            'attributes': {
                'target': self.target,
                'url': self.url,
            },
            'text': self.name
        }
