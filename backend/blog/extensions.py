#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   extensions.py
@Time    :   2024/08/19 11:18:08
@Author  :   Alan
@Desc    :   extensions
'''
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis


db = SQLAlchemy()
redis_client = FlaskRedis(decode_responses=True)