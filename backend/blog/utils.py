#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2024/08/19 15:13:10
@Author  :   Alan
@Desc    :   None
'''
import os
import random
import typing as t
import uuid
import time
from typing import Protocol

from flask import current_app
from apiflask import HTTPTokenAuth
from authlib.jose import jwt, JoseError
from authlib.jose.errors import ExpiredTokenError
from captcha.image import ImageCaptcha

from blog.extensions import db, redis_client
from blog.models.user import User
from blog.errors import TokenInvalidError, TokenExpiredError


auth = HTTPTokenAuth()


def get_auth_token(user):
    token_str, exp = user.get_token()
    return dict(
        token_str=token_str,
        expired_at=exp
    )


@auth.verify_token
def verify_token(token: str) -> t.Union[User, None]:
    # TODO: auth user 1 here, in order to be convenient with developing
    if os.getenv('FLASK_ENV') == 'development':
        return db.get_or_404(User, 1)
    try:
        # jwt.decode meth return claims_cls instance(default is JWTClaims)
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY']
        )
        # validate token, specially expire
        data.validate(leeway=30)
        id = data['id']
        user = db.get_or_404(User, id)
    except ExpiredTokenError:
        raise TokenExpiredError
    except (JoseError, IndexError):
        raise TokenInvalidError
    return user


def generate_random_numeric_str(long: int = 6) -> str:
    return ''.join(['%s' % random.randint(0, 9) for _ in range(long)])


def generate_captcha():
    opts = current_app.config['IMAGE_CAPTCHA_OPTS']
    width, height = opts['size']
    image_captcha = ImageCaptcha(width=width, height=height)
    image_captcha.character_offset_dx = opts['character_offset_dx']
    image_captcha.character_offset_dy = opts['character_offset_dy']
    image_captcha.character_rotate = opts['character_rotate']
    image_captcha.word_space_probability = opts['word_space_probability']
    image_captcha.word_offset_dx = opts['word_offset_dx']

    captcha_text = generate_random_numeric_str()
    captcha_image_id = uuid.uuid4().hex
    captcha_image_filename = f'{captcha_image_id}.png'
    captcha_image_url = f'temp/captcha/{captcha_image_filename}'
    captcha_image_path = os.path.join(
        current_app.config['CAPTCHA_PATH'],
        captcha_image_filename
    )
    image_captcha.write(
        format='png',
        chars=captcha_text,
        output=captcha_image_path
    )

    r_key = f'{current_app.config['CAPTCHA_REDIS_PREFIX']}_{captcha_image_id}'
    pipeline = redis_client.pipeline()
    pipeline.set(r_key, captcha_text)
    pipeline.expireat(r_key, int(time.time()) +
                      current_app.config['CAPTCHA_EXPIRED_TIME'])
    pipeline.execute()
    return captcha_image_id, captcha_image_url


def verify_captcha(captcha_image_id: str, answer: str) -> bool:
    r_key = f'{current_app.config['CAPTCHA_REDIS_PREFIX']}_{captcha_image_id}'
    data = redis_client.get(r_key)
    if data and data == answer:
        redis_client.delete(r_key)
        os.remove(os.path.join(
            current_app.config['CAPTCHA_PATH'], f'{captcha_image_id}.png'))
        return True
    return False


def f_success_response(data: t.Any = '', code: int = 0, message: str = 'ok'):
    return {'code': code, 'data': data, 'message': message}


def f_fail_response(data: t.Any = '', code: int = 1, message: str = 'failed'):
    return {'code': code, 'data': data, 'message': message}


class PaginationType(Protocol):
    page: int
    per_page: int
    pages: int
    total: int
    next_num: int
    has_next: bool
    prev_num: int
    has_prev: bool


def pagination_builder(pagination: PaginationType) -> dict:
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'page': pagination.page,
        'per_page': pagination.per_page
    }
