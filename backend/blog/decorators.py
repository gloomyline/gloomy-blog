#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   decorators.py
@Time    :   2024/08/26 09:30:31
@Author  :   Alan
@Desc    :   None
'''
import functools
from apiflask import abort
from apiflask.scaffold import _annotate as annotate, _ensure_sync as ensure_sync

from blog.utils import auth


def permission_required(permission_name):
    def decorator(f):
        f = ensure_sync(f)
        annotate(f)

        @functools.wraps(f)
        def decorated(*args, **kwargs):
            if not auth.current_user.can(permission_name):
                abort(status_code=403, message='权限不够', detail='当前账号角色权限不允许')
            return f(*args, **kwargs)
        return decorated
    return decorator


def admin_required(f):
    return permission_required('ADMIN')(f)
