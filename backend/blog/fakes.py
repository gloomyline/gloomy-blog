#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   fakes.py
@Time    :   2024/08/19 16:03:52
@Author  :   Alan
@Desc    :   None
'''
from faker import Faker

from sqlalchemy.exc import IntegrityError

from blog.extensions import db
from blog.models.user import User


fake = Faker()


def fake_user(count=10):
    for i in range(count):
        user = User(
            name=fake.name(),
            secret=fake.word(),
            username=fake.user_name(),
        )
        user.set_password('admin@520')
        db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()