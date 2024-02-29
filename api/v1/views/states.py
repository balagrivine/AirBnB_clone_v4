#!/usr/bin/python3

"""Creating a new view for State objects"""

from models.state import State
from models import storage
from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views

@app_views.route('/states/', methods=['GET'])
def all_states():
    """Retureves the list of all states objects"""
    list_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(list_states)

@app_views.route('/states/<state_id>', methods=['GET'])
def linked_states(state_id):
    """Retrieves states linked to the state ID"""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    return jsonify(state_obj[0])

@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """deletes a state based on its stateID"""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]

    """Raise a 404 error if state_id isn't linked to any state"""
    if state_obj == []:
        abort(404)

    state_obj.remove(state_obj[0])
    for obj in all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200

@app_views.route('/states/', methods=['POST'])
def create_state():
    """Creates  astate"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_states(state_id):
    """Updates a state object"""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(400)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200

