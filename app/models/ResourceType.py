# -*- coding: utf-8  -*-
# @Author: ty
# @File name: ResourceType.py 
# @IDE: PyCharm
# @Create time: 12/19/20 6:41 PM
from datetime import datetime

from flask_login import UserMixin

from app import db


class ResourceType(db.Model, UserMixin):
    """资源类型模型类"""
    __tablename__ = 'db_resource_type'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True, default=datetime.now)

    resources = db.relationship('Resource', backref='type', lazy='dynamic')

    def __repr__(self):
        return '<ResourceType $s>\n' % (self.name)

    def to_join(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'create_time': self.create_time,
            'update_time': self.update_time,
        }
