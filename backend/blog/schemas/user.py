# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2024/08/23 13:34:38
@Author  :   Alan
@Desc    :   None
'''
import os
from apiflask import Schema, PaginationSchema
from apiflask.fields import Integer, String, Nested, List
from apiflask.validators import Length

from blog.settings import config


env = os.getenv('FLASK_ENV', 'development')


class RoleInfo(Schema):
    id = Integer(description='角色id')
    name = String(descripton='角色名')


class UserInfo(Schema):
    id = Integer(description='用户id')
    name = String(description='用户姓名')
    username = String(description='用户名/账号')
    role = Nested(RoleInfo)


class UserEditIn(Schema):
    name = String(description='用户姓名', validate=[Length(6, 16)])
    role_id = Integer(desciption='角色名')


class UserCreateIn(Schema):
    username = String(
        required=True,
        validate=[Length(6, 16)],
        description='用户名/账号'
    )
    name = String(
        required=True,
        validate=[Length(6, 18)],
        description='用户姓名'
    )
    password = String(
        required=False,
        validate=[Length(6, 18)],
        description='密码',
        load_default='123456'
    )
    role_id = Integer(
        required=False,
        description='角色id',
        load_default=1
    )


class UserQuery(Schema):
    page = Integer(load_default=1, description='页码')
    per_page = Integer(
        load_default=config[env].USERS_PAGE_SIZE,
        description='用户列表页长'
    )


class UserList(Schema):
    items = List(Nested(UserInfo))
    pagination = Nested(PaginationSchema)
