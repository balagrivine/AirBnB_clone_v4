#!/usr/bin/python3

"""index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"users": "User", "places": "Place", "states": "State", "cities": "City",
            "amenities": "Amenity", "reviews": "Review"}

@app_views.route('/status')
def status():
    """returns a JSON"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def number_objects():
    """Retrieves the number of each objects by type"""
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
