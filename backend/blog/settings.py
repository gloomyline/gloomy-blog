#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   settings.py
@Time    :   2024/08/19 11:09:40
@Author  :   Alan
@Desc    :   None
'''
import os
import sys
import secrets

from blog.schemas.common import BaseResponse


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_urlsafe(16))

    '''
    link: https://apiflask.com/schema/#base-response-schema-customization
    Insert the output data into a data field and add some meta fields by
    passing the customized base response schema to it
    '''
    BASE_RESPONSE_SCHEMA = BaseResponse
    '''
    The default data key is "data", you can change it to match your data
    field name in your schema via the configuration variable BASE_RESPONSE_DATA_KEY:
    '''
    BASE_RESPONSE_DATA_KEY = 'data'

    CACHE_TYPE = 'redis'

    IMAGE_CAPTCHA_OPTS = {
        'size': (280, 90),
        'character_offset_dx': (0, 4),
        'character_offset_dy': (0, 6),
        'character_rotate': (-40, 40),
        'word_space_probability': 0.5,
        'word_offset_dx': 0.25
    }
    CAPTCHA_PATH = os.path.join(basedir, 'temp/captcha')
    CAPTCHA_EXPIRED_TIME = 5 * 60
    CAPTCHA_REDIS_PREFIX = 'blog_captcha'

    AUTH_TOKEN_EXPIRED_TIME = 24 * 60 * 60

    USERS_PAGE_SIZE = 10

    TAGS = [
        {'name': 'TokenAuth', 'description': '登录认证'},
        {'name': 'User', 'description': '用户模块'},
        {'name': 'Main', 'description': '主要模块'},
    ]
    SERVERS = [
        {'name': 'Development Server', 'url': 'http://localhost:5000'},
        {'name': 'Production server', 'url': 'http://api.blog.com'},
        {'name': 'Testing Server', 'url': 'http://test.example.com'}
    ]
    EXTERNAL_DOCS = {
        'description': 'Powered by ==APIFlask== Find more info here.',
        'url': 'https://apiflask.com/docs'
    }
    INFO = {
        'title': 'BlogApi',
        'version': '1.0.0',
        'description': 'The apis of my blog.',
        'contact': {
            'name': 'AlanWang',
            'url': 'https://github.com/gloomyline',
            'email': '1211071880@qq.com'
        },
        'license': {
            'name': 'MIT',
            'url': 'https://mit-license.org/'
        }
    }
    '''
    View the spec from your browser via /openapi.json, the indentation will set to 2
    which is the default value to the config `LOCAL_SPEC_JSON_INDENT`(i.e.,2).
    When use the flask spec command, change the indentation with the `--indent` or `-i` option
    '''
    JSONIFY_PRETTYPRINT_REGULAR = True
    # enable the local spec file to be syncronized with the project code
    SYNC_CONFIG_SEPC = True
    LOCAL_SPEC_PATH = os.path.join(basedir, 'openapi.json')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    REDIS_URL = 'redis://localhost:6379'


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
