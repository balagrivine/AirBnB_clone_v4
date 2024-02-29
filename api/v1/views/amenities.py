#!/usr/bin/python3

"""Creating a new view for State objects"""

from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    """Retureves the list of all states objects"""
    all_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(all_amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities(amenity_id):
    """Retrieves amenities linked to the amenity ID"""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj[0])

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    """deletes an amenity based on its stateID"""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities if obj.id == amenity_id]

    """Raise a 404 error if state_id isn't linked to any state"""
    if amenity_obj == []:
        abort(404)

    amenity_obj.remove(amenity_obj[0])
    for obj in all_amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200

@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """Creates  astate"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenities(amenity_id):
    """Updates a state object"""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities if obj.id == amenity_id]
    if amenity_obj == []:
        abort(400)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity_obj[0]['name'] = request.json['name']
    for obj in all_amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity_obj[0]), 200

