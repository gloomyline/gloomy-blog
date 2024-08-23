#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   auth.py
@Time    :   2024/08/19 14:05:41
@Author  :   Alan
@Desc    :   None
'''
from apiflask import APIBlueprint, abort

from blog.extensions import db
from blog.models.user import User
from blog.schemas.user import UserInfo
from blog.schemas.auth import Captcha, Login, LoginInfo
from blog.errors import TokenInvalidError
from blog.utils import auth, generate_captcha, get_auth_token, verify_captcha, \
    f_success_response, f_fail_response


auth_bp = APIBlueprint('auth', __name__, tag='TokenAuth', url_prefix='/auth')


@auth_bp.post('/captcha')
@auth_bp.output(Captcha, description='图形验证码')
@auth_bp.doc(tags=['TokenAuth'])
def get_captcha():
    '''获取图形验证码

    生成有有效期的图形验证码
    有效期为`current_app.config['CAPTCHA_EXPIRED_TIME']`
    单位为秒(second)
    '''
    captcha_key, captcha_path = generate_captcha()
    data = {
        'captcha_key': captcha_key,
        'captcha': captcha_path
    }
    return f_success_response(data)


@auth_bp.post('/login')
@auth_bp.input(Login)
@auth_bp.output(LoginInfo, description='登录响应，成功返回用户信息和token')
@auth_bp.doc(tags=['TokenAuth'])
def login(json_data):
    '''登录

    使用账号、密码和图形验证码登录
    '''
    username = json_data['username']
    password = json_data['password']
    captcha = json_data['captcha']
    captcha_key = json_data['captcha_key']
    if not verify_captcha(captcha_key, captcha):
        return f_fail_response(message='验证码不正确或已过期')

    user = db.first_or_404(db.select(User).filter_by(username=username))
    if not user.validate_password(password):
        return f_fail_response(message='密码错误或账号不存在')

    data = {'userinfo': user, 'token': get_auth_token(user)}
    return f_success_response(data)


@auth_bp.post('/logout')
@auth_bp.auth_required(auth)
@auth_bp.doc(tags=['TokenAuth'])
def logout():
    '''退出登录

    需要客户端自行维护token,清除token
    '''
    return f_success_response(message='退出登录成功')


@auth_bp.get('/userinfo')
@auth_bp.auth_required(auth)
@auth_bp.output(UserInfo, description='用户信息')
@auth_bp.doc(tags=['TokenAuth'])
def get_user_info():
    '''获取当前用户信息

    获取当前认证用户信息
    '''
    return f_success_response(auth.current_user)
