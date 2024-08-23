#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2024/08/23 09:47:30
@Author  :   Alan
@Desc    :   None
'''
from apiflask import APIBlueprint
from flask.views import MethodView


user_bp = APIBlueprint('user', __name__)


class UserController(MethodView):
    pass


user_bp.add_url_rule('/user', view_func=UserController.as_view('user'))
