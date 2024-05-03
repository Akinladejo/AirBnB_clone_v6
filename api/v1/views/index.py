#!/usr/bin/python3
"""index Module"""
from flask import Blueprint, jsonify
from models import storage

app_views = Blueprint('app_views', __name__)

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"}), 200

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of objects for each model type"""
    models = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(models), 200
