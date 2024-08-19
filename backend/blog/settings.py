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


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_urlsafe(16))

    TAGS = [
        {'name': 'Main', 'description': 'The description of the **Main** tag.'},
        {'name': 'TokenAuth', 'description': 'The description of the **TokenAuth** tag.'}
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


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}