#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/08/19 13:16:11
@Author  :   Alan
@Desc    :   None
'''
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetIn(Schema):
    name = String(
        required=True,
        validate=Length(1, 10),
        metadata={'title': 'Pet Name', 'description': 'The name of the pet.'}
    )
    category = String(
        required=True,
        validate=OneOf(['dog', 'cat']),
        metadata={'title': 'Pet Category',
                  'description': 'The category of the pet.'}
    )


class PetOut(Schema):
    id = Integer(metadata={'title': 'Pet ID',
                 'description': 'The ID of the pet.'})
    name = String(metadata={'title': 'Pet Name',
                  'description': 'The name of the pet.'})
    category = String(
        metadata={'title': 'Pet Category', 'description': 'The category of the pet.'})
