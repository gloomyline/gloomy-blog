#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   auth.py
@Time    :   2024/08/19 14:11:59
@Author  :   Alan
@Desc    :   None
'''
from apiflask import Schema
from apiflask.fields import Integer, String, Nested
from apiflask.validators import Length

from blog.schemas.main import UserInfo


class Captcha(Schema):
    captcha = String(description='验证码图片url')
    captcha_key = String(description='验证码key')


class Login(Schema):
    username = String(
        required=True,
        validate=[Length(6, 16)],
        description='用户名/账号',
    )
    password = String(
        required=True,
        validate=[Length(6, 18)],
        description='密码'
    )
    captcha = String(
        required=True,
        validate=Length(6),
        description='图形验证码'
    )    
    captcha_key = String(
        required=True,
        description='图形验证码key'
    )


class Token(Schema):
    token_str = String()
    expired_at = Integer(description='token过期时间戳')


class LoginInfo(Schema):
    userinfo = Nested(UserInfo)
    token = Nested(Token)

