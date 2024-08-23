#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   post.py
@Time    :   2024/08/22 14:56:22
@Author  :   Alan
@Desc    :   None
'''
from datetime import datetime, UTC

from blog.extensions import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(UTC), index=True, comment='创建时间')

    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = db.get_or_404(Category, 1)
        posts = self.posts[:]
        for post in posts:
           post.category = default_category
        db.session.delete(self)
        db.session.commit()


post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(UTC), index=True, comment='创建时间')

    posts = db.relationship('Post', secondary=post_tag, back_populates='tags')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, comment='标题')
    sub_title = db.Column(db.String(256), comment='副标题')
    body = db.Column(db.Text, comment='文章内容')
    timestamp = db.Column(db.DateTime, default=datetime.now(UTC), index=True, comment='创建时间')
    can_comment = db.Column(db.Boolean, default=True, comment='是否可以评论')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), comment='分类id')

    category = db.relationship('Category', back_populates='posts')
    tags = db.relationship('Tag', secondary=post_tag, back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade=['all', 'delete-orphan'])


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, comment='评论内容')
    timestamp = db.Column(db.DateTime, default=datetime.now(UTC), index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    post = db.relationship('Post', back_populates='comments')
    replies = db.relationship('Comment',
                              backref=db.backref('replied', remote_side=[id]), cascade=['all', 'delete-orphan'])

    