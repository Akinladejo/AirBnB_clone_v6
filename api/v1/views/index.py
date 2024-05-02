#!/usr/bin/python3
"""Defines endpoints for retrieving status and statistics."""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns JSON response with status OK."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Returns JSON response with counts of each instance type."""
    amenity_count = storage.count("Amenity")
    city_count = storage.count("City")
    place_count = storage.count("Place")
    review_count = storage.count("Review")
    state_count = storage.count("State")
    user_count = storage.count("User")

    stats_dict = {
        "amenities": amenity_count,
        "cities": city_count,
        "places": place_count,
        "reviews": review_count,
        "states": state_count,
        "users": user_count
    }

    return jsonify(stats_dict)
