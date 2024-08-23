#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024/08/19 10:18:17
@Author  :   Alan
@Desc    :   apiflask package main
'''
import os
import click

from apiflask import APIFlask

from blog.extensions import db, redis_client
from blog.settings import config
from blog.models.user import Role
from blog.blueprints.main import main_bp
from blog.blueprints.auth import auth_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = APIFlask('blog')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_error_handler(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    redis_client.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)


def register_error_handler(app):
    @app.error_processor
    def error_handler(error):
        return {
            'code': error.status_code,
            'message': error.message,
            'detail': error.detail
        }, error.status_code, error.headers


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                click.style('This operation will delete the database, stll continue?', fg='bright_red'),
                abort=True
            )
            db.drop_all()
            click.echo(click.style('Drop tables.', fg='blue'))
            db.create_all()
            click.secho('Initialized database.', fg='bright_green')

    @app.cli.command()
    def init():
        """Initialize blog."""
        db.create_all()
        click.secho('Initialized database.', fg='bright_green')
        Role.init_role()
        click.secho('Intializing the roles and permissions...', fg='bright_blue')
        from blog.fakes import fake_admin
        fake_admin()


    @app.cli.command()
    @click.option('--user', default=10, help='Quantity of users, default is 10.')
    @click.option('--cate', default=10, help='Quantity of categories of post, default is 10.')
    @click.option('--tag', default=10, help='Quantity of tags of post, default is 10.')
    @click.option('--post', default=10, help='Quantity of posts, default is 10.')
    def forge(user, cate, tag, post):
        """Generate fake data."""
        db.drop_all()
        db.create_all()

        Role.init_role()
        click.secho('Intializing the roles and permissions...', fg='bright_blue')
        from blog.fakes import fake_admin, fake_user, fake_category, \
            fake_tag, fake_post
        fake_admin()
        click.secho('Generating admin', fg='red')
        fake_user(user)
        click.secho('Generating %d users...' % user, fg='blue')   
        fake_category(cate)
        click.secho('Generating %d cates...' % cate, fg='blue')   
        fake_tag(tag)
        click.secho('Generating %d tags...' % tag, fg='blue')   
        fake_post(post)
        click.secho('Generating %d posts...' % post, fg='blue')   