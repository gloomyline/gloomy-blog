#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   fakes.py
@Time    :   2024/08/19 16:03:52
@Author  :   Alan
@Desc    :   None
'''
import random

from faker import Faker

from sqlalchemy.exc import IntegrityError

from blog.extensions import db
from blog.models import Role, User, Post, Category, Tag


fake = Faker()


def fake_admin():
    role_admin = db.session.execute(
        db.select(Role).filter_by(name='Admin')).scalar()
    admin = User(
        name='AlanWang',
        username='gloomyline',
        role=role_admin
    )
    admin.set_password('admin@520')
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    for i in range(count):
        user = User(
            name=fake.name(),
            username=fake.user_name(),
        )
        user.set_password('123456')
        db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def fake_category(count=10):
    for i in range(count):
        category = Category(
            name=fake.word(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_tag(count=10):
    for i in range(count):
        tag = Tag(
            name=fake.word(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(tag)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def fake_post(count=10):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            sub_title=fake.sentence(),
            body=fake.text(1000),
            category=Category.query.get(
                random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        for j in range(random.randint(1, 5)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            if tag not in post.tags:
                post.tags.append(tag)

        db.session.add(post)
    db.session.commit()
