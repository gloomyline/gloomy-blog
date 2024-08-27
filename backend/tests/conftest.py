#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   conftest.py
@Time    :   2024/08/26 14:06:53
@Author  :   Alan
@Desc    :   None
'''
import pytest

from blog import create_app
from blog.extensions import db
from blog.models import Role


@pytest.fixture
def app():
    app = create_app('testing')

    test_request_context = app.test_request_context()
    test_request_context.push()
    db.create_all()
    Role.init_role()

    yield app

    db.drop_all()
    test_request_context.pop()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
