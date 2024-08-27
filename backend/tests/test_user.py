#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test_user.py
@Time    :   2024/08/26 17:35:39
@Author  :   Alan
@Desc    :   None
'''


def test_get_user_list(client):
    response = client.get('/users', json={})
    assert response.status_code == 200
    assert response.get_json()['data']['items'] == []
