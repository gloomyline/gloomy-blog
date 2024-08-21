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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    secret = db.Column(db.String(10))
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(255))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_token(self) -> str:
        now = int(time.time())
        exp = now + current_app.config['AUTH_TOKEN_EXPIRED_TIME']
        header = {'alg': 'HS256', 'type': 'JWT'}
        payload = {'id': self.id, 'exp': exp}
        return jwt.encode(header, payload, current_app.config['SECRET_KEY']).decode(), exp
