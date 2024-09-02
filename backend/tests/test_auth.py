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
from flask import current_app


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


def test_logout():
    pass


def test_get_userinfo(login):
    pass
