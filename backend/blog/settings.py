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


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig():
    TAGS = [
        {'name': 'Main', 'description': 'The description of the **Main** tag.'}
    ]
    SERVERS = [
        {'name': 'Development Server', 'url': 'http://localhost:5000'},
        {'name': 'Production server', 'url': 'http://api.blog.com'},
        {'name': 'Testing Server', 'url': 'http://test.example.com'}
    ]
    EXTERNAL_DOCS = {
        'description': 'Find more info here.',
        'url': 'https://apiflask.com/docs'
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