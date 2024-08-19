#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   auth.py
@Time    :   2024/08/19 14:11:59
@Author  :   Alan
@Desc    :   None
'''
from apiflask import Schema
from apiflask.fields import String


class Token(Schema):
    token = String()