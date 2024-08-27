#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test_main.py
@Time    :   2024/08/26 17:21:01
@Author  :   Alan
@Desc    :   None
'''


def test_get_pet(app, client):
    response = client.get('/pets/1', json={})
    json_data = response.get_json()
    data = json_data['data']
    assert data['id'] == 1
    assert data['category'] == 'dog'
    assert data['name'] == 'Coco'
