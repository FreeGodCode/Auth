# -*- coding: utf-8  -*-
# @Author: ty
# @File name: __init__.py 
# @IDE: PyCharm
# @Create time: 12/19/20 4:55 PM
from datetime import datetime

from flask_login import UserMixin

from app import db
# 角色资源关联表
role_resource_table = db.Table(
    'db_role_resource',
    db.metadata,
    db.Column('role_id', db.String, db.ForeignKey('role.id'))
)


class Role(db.Model, UserMixin):
    """角色模型类"""
    __tablename__ = 'db_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(256))
    icon = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True, default=datetime.now)
    seq = db.Column(db.Integer)
    # 包含资源
    resources = db.relationship('Resource',
                                secondary=role_resource_table,
                                backref=db.backref('db_role', lazy='dynamic'))

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        """
        排除私有属性
        :return:
        """
        return dict([(k, getattr(self, k)) for k in self.__dict__.keys() if not k.startswith("_")])

    def __repr__(self):
        """
        格式化输出字符
        :return:
        """
        return '<Role name: %s desc: %s icon: %s seq:%s>\n' %(self.name, self.desc, self.icon, self.seq)

    def to_join(self):
        return {
            'id': self.id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'name': self.name,
            'desc': self.desc,
            'icon': self.icon,
            'seq': self.seq,
        }