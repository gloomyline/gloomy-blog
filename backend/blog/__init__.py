#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024/08/19 10:18:17
@Author  :   Alan
@Desc    :   apiflask package main
'''
import os

from apiflask import APIFlask

from blog.extensions import db
from blog.settings import config
from blog.blueprints.main import main_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = APIFlask('blog')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)