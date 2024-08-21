#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/08/19 11:26:33
@Author  :   Alan
@Desc    :   None
'''
from apiflask import APIBlueprint, abort

from blog.schemas.main import PetIn, PetOut


main_bp = APIBlueprint('main', __name__)

pets = [
    {'id': 0, 'name': 'Kitty', 'category': 'cat'},
    {'id': 1, 'name': 'Coco', 'category': 'dog'},
    {'id': 2, 'name': 'Flash', 'category': 'cat'},
]


@main_bp.route('/')
@main_bp.doc(tags=['Main'])
def index():
    """Just Say Hello

    It will always return a greeting like this:
    ```
    {'message': 'Hello!'}
    ```
    """
    return {'message': 'hello'}


@main_bp.get('/pets/<int:pet_id>')
@main_bp.output(PetOut, description='The pet with given ID.')
@main_bp.doc(tags=['Main'], operation_id='getPet')
def get_pet(pet_id):
    """Get a Pet

    Get a pet with specific ID.
    """
    if pet_id > len(pets) - 1 or pets[pet_id].get('deleted'):
        abort(404)
    return { 'code': 0, 'data': pets[pet_id], 'message': 'ok' }


@main_bp.get('/pets')
@main_bp.output(PetOut(many=True), description='A list of pets.')
@main_bp.doc(tags=['Main'], operation_id='getPets')
def get_pets():
    """Get All Pet

    Get all pets in the database.
    """
    return { 'code': 0, 'data': pets, 'message': 'ok' }


@main_bp.post('/pets')
@main_bp.input(PetIn, location='json')
@main_bp.output(
    PetOut,
    status_code=201,
    description='The pet you just created',
    links={'getPetById': {'operationId': 'getPet', 'parameters': {'pet_id': '$response.body#/id'}}}
)
@main_bp.doc(tags=['Main'])
def create_pet(json_data):
    """Create a Pet

    Create a pet with given data. The created pet will be returned.
    """
    pet_id = len(pets)
    json_data['id'] = pet_id
    pets.append(json_data)
    return pets[pet_id]


@main_bp.patch('/pets')
@main_bp.input(PetIn(partial=True), location='json')
@main_bp.output(PetOut, description='The updated pet.')
@main_bp.doc(tags=['Main'])
def update_pet(pet_id, json_data):
    """Update a Pet

    Update a pet with given data, the valid fields are `name` and `category`.
    """
    if pet_id > len(pets) - 1:
        abort(404)
    for attr, value in json_data.items():
        pets[pet_id][attr] = value
    return pets[pet_id]


@main_bp.delete('/pets/<int:pet_id>')
@main_bp.output({}, status_code=204)
@main_bp.doc(tags=['Main'])
def delete_pet(pet_id):
    """Delete a Pet

    Delete a pet with specific ID. The deleted pet will be renamed to `"Ghost"`.
    """
    if pet_id > len(pets) - 1:
        abort(404)
    pets[pet_id]['deleted'] = True
    pets[pet_id]['name'] = 'Ghost'
    return ''