# -*- coding: utf-8  -*-
# @Author: ty
# @File name: OnLine.py 
# @IDE: PyCharm
# @Create time: 12/19/20 6:42 PM
from datetime import datetime

from app import db


class OnLine(db.Model):
    """"""
    __tablename__ = 'db_online'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(128))
    ip = db.Column(db.String(64))
    type = db.Column(db.String(1))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<OnLine %s>\n' % (self.nickname)

    def to_json(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'ip': self.ip,
            'type': self.type,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

