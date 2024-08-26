#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2024/08/23 09:47:30
@Author  :   Alan
@Desc    :   None
'''
from apiflask import APIBlueprint
from flask.views import MethodView

from blog.extensions import db
from blog.models import User
from blog.schemas.user import UserCreateIn, UserEditIn, UserInfo, UserList, UserQuery
from blog.utils import auth, f_success_response, f_fail_response, pagination_builder
from blog.decorators import admin_required


user_bp = APIBlueprint('user', __name__)


class UserController(MethodView):
    decorators = [user_bp.auth_required(auth)]

    @user_bp.output(UserInfo)
    @user_bp.doc(tags=['User'])
    def get(self, id):
        """获取用户信息

        根据用户id获取用户信息
        """
        user = db.get_or_404(User, id)
        return f_success_response(user)

    @user_bp.input(UserEditIn(partial=True), location='json')
    @user_bp.output(UserInfo)
    def patch(self, id, json_data):
        """修改用户信息

        根据用户id修改用户信息
        """
        user = db.get_or_404(User, id)
        for attr, value in json_data.items():
            setattr(user, attr, value)
        db.session.commit()
        return f_success_response(user)

    @user_bp.output({})
    def delete(self, id):
        """删除用户

        根据用户id删除用户信息
        """
        user = db.get_or_404(User, id)
        db.session.delete(user)
        db.session.commit()
        return f_success_response()


class UsersController(MethodView):
    decorators = [user_bp.auth_required(auth)]

    @user_bp.input(UserQuery, location='query')
    @user_bp.output(UserList)
    @user_bp.doc(tags=['User'])
    def get(self, query_data):
        """用户列表

        分页查询 page, per_page
        """
        pagination = db.paginate(db.select(User), **query_data)
        users = pagination.items
        return f_success_response({'items': users, 'pagination': pagination_builder(pagination)})

    @admin_required
    @user_bp.input(UserCreateIn, location='json')
    @user_bp.output(UserInfo)
    def post(self, json_data):
        '''创建用户

        **Admin**创建新用户
        '''
        username = json_data['username']
        name = json_data['name']
        role_id = json_data['role_id']
        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()
        if user is not None:
            return f_fail_response(message='用户名已存在')

        user = db.session.execute(
            db.select(User).filter_by(name=name)
        ).scalar_one_or_none()
        if user is not None:
            return f_fail_response(message='姓名已存在')

        user = User(username=username, name=name, role_id=role_id)
        user.set_password(json_data['password'])
        db.session.add(user)
        db.session.commit()
        return f_success_response(user)


user_bp.add_url_rule(
    '/user/<int:id>', view_func=UserController.as_view('user'))
user_bp.add_url_rule('/users', view_func=UsersController.as_view('users'))
