# -*- coding: utf-8  -*-
# @Author: ty
# @File name: Organization.py 
# @IDE: PyCharm
# @Create time: 12/19/20 6:41 PM
from datetime import datetime

from flask_login import UserMixin

from app import db

# 组织资源关联表
organization_resource_table = db.Table('db_organization_resource',
                                       db.metadata,
                                       db.Column('resource_id', db.String, db.ForeignKey('db_resource.id')),
                                       db.Column('organization_id', db.String, db.ForeignKey('db_organization.id'))
                                       )


class Organization(db.Model, UserMixin):
    """组织模型类"""
    __tablename__ = 'db_organization'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    address = db.Column(db.String(256))
    code = db.Column(db.String(256))
    icons = db.Column(db.String(256))
    seq = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True, default=datetime.now)

    resources = db.relationship('Resource',
                                secondary=organization_resource_table,
                                backref=db.backref('db_organization', lazy='dynamic'))

    organization_id = db.Column(db.Integer, db.ForeignKey('db_organization.id'))

    parent = db.relationship('Organization', remote_side=[id], backref='db_organization', uselist=False)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Organization %s>\n' % (self.name)

    def get_pid(self):
        if self.parent:
            return self.parent.id
        return ''

    def to_join(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'code': self.code,
            'icons': self.icons,
            'seq': self.seq,
            'pid': self.get_pid(),
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
