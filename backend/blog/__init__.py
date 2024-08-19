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

from blog.extensions import db
from blog.settings import config
from blog.blueprints.main import main_bp
from blog.blueprints.auth import auth_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = APIFlask('blog')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)


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
    @click.option('--user', default=10, help='Quantity of users, default is 10.')
    def forge(user):
        """Generate fake data."""
        from blog.fakes import fake_user
    
        db.drop_all()
        db.create_all()

        click.secho('Generating %d users...' % user, fg='blue')
        fake_user(user)