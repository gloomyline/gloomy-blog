#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   conftest.py
@Time    :   2024/08/26 14:06:53
@Author  :   Alan
@Desc    :   None
'''
import json
import pytest
from flask import current_app, url_for

from blog import create_app
from blog.extensions import db, redis_client
from blog.models import Role, User, Category, Post, Tag


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
def init_test_data():
    admin_user = User(name='Admin User', username='adminuser', role_id=1)
    admin_user.set_password('123456')
    normal_user = User(name='Normal User', username='normaluser', role_id=2)
    normal_user.set_password('123456')

    category_primary = Category(name='primary')
    category_secondary = Category(name='secondary')
    tag = Tag(name='default_tag')

    post = Post(
        title='test title',
        sub_title='test sub title',
        body='test body',
        can_comment=True,
        category=category_primary,
    )
    post.tags.append(tag)
    post2 = Post(
        title='test title 2',
        sub_title='test sub title 2',
        body='test body 2',
        can_comment=True,
        category=category_secondary,
    )
    db.session.add_all(
        [admin_user, normal_user, category_primary, category_secondary, post, post2])
    db.session.commit()


@pytest.fixture
def client(app, init_test_data):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def login(request, client):
    if not hasattr(request, 'param') or request.param is None:
        username = 'adminuser'
        password = '123456'
    else:
        param = request.param
        username = param['username']
        password = param['password']

    response = client.post(url_for('auth.get_captcha'), json={})
    captcha_key = response.get_json()['data']['captcha_key']
    r_key = f'{current_app.config['CAPTCHA_REDIS_PREFIX']}_{captcha_key}'
    captcha_text = redis_client.get(r_key)

    body = {
        'username': username,
        'password': password,
        'captcha_key': captcha_key,
        'captcha': captcha_text
    }
    return client.post(url_for('auth.login'), json=body)


@pytest.fixture
def logout(client):
    return client.post(url_for('auth.logout'))
