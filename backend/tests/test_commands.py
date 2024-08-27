#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test_commands.py
@Time    :   2024/08/26 14:35:26
@Author  :   Alan
@Desc    :   None
'''
from blog.extensions import db
from blog.models import User, Category, Tag, Post


def test_initdb(runner):
    result = runner.invoke(args='initdb')
    assert 'Initialized database.' in result.output


def test_initdb_with_drop(runner):
    result = runner.invoke(args=['initdb', '--drop'], input='y\n')
    assert 'This operation will delete the database, stll continue?' in result.output
    assert 'Drop tables.' in result.output


def test_init(runner):
    result = runner.invoke(args='init')
    assert 'Initialized database.' in result.output
    assert 'Intializing the roles and permissions...' in result.output
    assert 'Done.' in result.output


def test_forge():
    pass


def test_forge_with_count(runner):
    result = runner.invoke(
        args=[
            'forge',
            '--user', '5',
            '--cate', '5',
            '--tag', '5',
            '--post', '20'
        ]
    )
    assert 'Intializing the roles and permissions...' in result.output

    assert db.session.query(User).count() == 5 + 1
    assert 'Generating admin' in result.output

    assert db.session.query(Category).count() == 5
    assert 'Generating 5 cates...' in result.output

    assert db.session.query(Tag).count() == 5
    assert 'Generating 5 tags...' in result.output

    assert db.session.query(Post).count() == 20
    assert 'Generating 20 posts...' in result.output

    assert 'Done.' in result.output
