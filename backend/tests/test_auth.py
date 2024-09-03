#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test_auth.py
@Time    :   2024/08/29 09:03:21
@Author  :   Alan
@Desc    :   None
'''
import pytest
import time
from flask import current_app, url_for


def test_get_captcha(client):
    response = client.get('/auth/captcha', json={})
    assert response.status_code == 405

    response = client.post('/auth/captcha', json={})
    assert response.status_code == 200
    result = response.get_json()
    assert result['code'] == 0
    assert 'ok' in result['message']
    data = result['data']
    assert data['captcha_key'] is not None
    assert data['captcha'] is not None


@pytest.mark.parametrize('login', [{'username': 'normaluser', 'password': '123456'}], indirect=True)
def test_login(login):
    result = login.get_json()
    assert result['code'] == 0
    assert result['message'] == 'ok'

    data = result['data']
    assert data['userinfo']['id'] == 2
    assert data['userinfo']['role']['id'] == 2
    assert data['token']['token_str'] is not None
    expired_at = data['token']['expired_at']
    assert int(time.time()) + \
        current_app.config['AUTH_TOKEN_EXPIRED_TIME'] >= expired_at


def test_logout(client, login):
    result = login.get_json()
    token = result['data']['token']['token_str']
    response = client.post(url_for('auth.logout'), headers={
                           'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert '退出登录成功' in response.get_json()['message']


def test_get_userinfo(client, login):
    response = client.get(url_for('auth.get_user_info'))
    assert response.status_code == 401

    token = login.get_json()['data']['token']['token_str']
    response = client.get(url_for('auth.get_user_info'), headers={
                          'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()['data']
    assert data['id'] == 1
    assert data['username'] == 'adminuser'
    assert data['name'] == 'Admin User'
    assert data['role']['id'] == 1
