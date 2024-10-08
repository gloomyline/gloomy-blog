
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   common.py
@Time    :   2024/08/20 11:06:11
@Author  :   Alan
@Desc    :   None
'''
from apiflask import Schema
from apiflask.fields import Integer, String, Field


class BaseResponse(Schema):
    code = Integer(metadata={'description': '自定义响应代码'})
    data = Field(metadata={'description': '请求响应数据'})
    message = String(metadata={'description': '请求响应简讯'})


class PaginationQuery(Schema):
    page = Integer(metadata={'description': '页码'})
    per_page = Integer(metadata={'description': '页长'})
