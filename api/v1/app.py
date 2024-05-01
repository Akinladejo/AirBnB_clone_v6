#!/usr/bin/python3
"""
App views for AirBnB_clone_v3
"""

from flask import Blueprint, jsonify
from models import storage

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ returns status """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    """ returns number of each objects by type """
    total = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}
    for cls in classes:
        count = storage.count(cls)
        total[classes.get(cls)] = count
    return jsonify(total)
