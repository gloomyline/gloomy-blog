#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2024/08/19 15:13:10
@Author  :   Alan
@Desc    :   None
'''
import typing as t

from flask import current_app
from apiflask import HTTPTokenAuth
from authlib.jose import jwt, JoseError

from blog.models.user import User


auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token: str) -> t.Union[User, None]:
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY']
        )
        id = data['id']
        user = User.query.get_or_404(id)
    except JoseError:
        return None
    except IndexError:
        return None
    return user