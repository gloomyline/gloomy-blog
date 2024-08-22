#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   errors.py
@Time    :   2024/08/22 09:16:21
@Author  :   Alan
@Desc    :   None
'''
from apiflask import HTTPError


class TokenInvalidError(HTTPError):
    status_code = 401
    message = '请登录'
    detail = 'token认证失败'


class TokenExpiredError(HTTPError):
    status_code = 402
    message = '登录失效，请重新登录'
    detail = 'token过期了'