#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2024/08/19 15:21:18
@Author  :   Alan
@Desc    :   None
'''
import time

from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from authlib.jose import jwt

from blog.extensions import db


role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    roles = db.relationship('Role', secondary=role_permission, back_populates='permissions')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=role_permission, back_populates='roles')

    def __repr__(self):
        return '%s_%d: %s' % (__class__.name, self.id, self.name)

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'Admin': ['COMMENT', 'UPLOAD', 'ADMIN'],
            'User': ['COMMENT'],
        }
        for role_name in roles_permissions_map:
            role = db.session.execute(db.select(Role).filter_by(name=role_name)).scalar()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
                role.permissions = []
                for permission_name in roles_permissions_map[role_name]:
                    permission = db.session.execute(db.select(Permission).filter_by(name=permission_name)).scalar()
                    if permission is None:
                        permission = Permission(name=permission_name)
                        db.session.add(permission)
                    role.permissions.append(permission)
        db.session.commit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role', back_populates='users')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_token(self):
        now = int(time.time())
        exp = now + current_app.config['AUTH_TOKEN_EXPIRED_TIME']
        header = {'alg': 'HS256', 'type': 'JWT'}
        payload = {'id': self.id, 'exp': exp}
        return jwt.encode(header, payload, current_app.config['SECRET_KEY']).decode(), exp

    def is_admin(self):
        return self.role.name == 'Admin'
