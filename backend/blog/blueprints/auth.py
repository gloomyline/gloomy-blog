#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   auth.py
@Time    :   2024/08/19 14:05:41
@Author  :   Alan
@Desc    :   None
'''

from apiflask import APIBlueprint, abort

from blog.utils import auth
from blog.schemas.auth import Token
from blog.models.user import User

auth_bp = APIBlueprint('auth', __name__, tag='TokenAuth', url_prefix='/auth')


@auth_bp.post('/token/<int:id>')
@auth_bp.output(Token, description='用户{id}的登录凭证token')
@auth_bp.doc(tags=['TokenAuth'])
def get_token(id: int):
    user = User.query.get_or_404(id)
    return {'token': user.get_token}


@auth_bp.get('/name/<int:id>')
@auth_bp.auth_required(auth)
@auth_bp.doc(tags=['TokenAuth'])
def get_secret(id):
    if auth.current_user.id == id:
        return auth.current_user.secret
    else:
        abort(401)
