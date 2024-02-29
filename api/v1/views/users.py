#!/usr/bin/python3

"""Creating a new view for State objects"""

from models import storage
from flask import jsonify, abort, request
from models.user import User
from api.v1.views import app_views

@app_views.route('/users', methods=['GET'])
@app_views.route('/users/', methods=['GET'])
def all_users():
    """Retureves the list of all states objects"""
    list_users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(list_users)

@app_views.route('/users/<user_id>', methods=['GET'])
def linked_users(user_id):
    """Retrieves states linked to the state ID"""
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    return jsonify(user_obj[0])

@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """deletes a state based on its stateID"""
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]

    """Raise a 404 error if state_id isn't linked to any state"""
    if user_obj == []:
        abort(404)

    user_obj.remove(user_obj[0])
    for obj in all_users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200

@app_views.route('/users/', methods=['POST'])
def create_user():
    """Creates  astate"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'password' not in request.get_json():
        abort(400, 'Missing password')

    if 'email' not in request.get_json():
        abort(400, 'Missing email')

    users = []
    new_user = User(email=request.json['email'],
                    password=request.json['password'],
                    first_name=request.json['first_name'],
                    last_name=request.json['last_name'])
    storage.new(new_user)
    storage.save()
    users.append(new_user.to_dict())
    return jsonify(users[0]), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_users(user_id):
    """Updates a state object"""
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        user_obj[0]['first_name'] = request.json['first_name']
    except:
        pass
    try:
        user_obj[0]['last_name'] = request.json['last_name']
    except:
        pass
    for obj in all_users:
        if obj.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    obj.first_name = request.json['first_name']
            except:
                pass
            try:
                if request.json['last_name'] is not None:
                    obj.last_name = request.json['last_name']
            except:
                pass
            try:
                if request.json['email'] is not None:
                    obj.email = request.json['email']
            except:
                pass
            try:
                if request.json['password'] is  not None:
                    obj.password = request.json['password']
            except:
                pass
    storage.save()
    return jsonify(user_obj[0]), 200

