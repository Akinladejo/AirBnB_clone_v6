#!/usr/bin/python3
""" View for Amenity objects that handles default API actions """
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def handle_amenities():
    """Handles GET and POST requests for amenities"""
    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        return jsonify([amenity.to_dict() for amenity in amenities]), 200
    elif request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, "Not a JSON")
        if 'name' not in req_data:
            abort(400, "Missing name")
        amenity = Amenity(**req_data)
        storage.new(amenity)
        storage.save()

        return jsonify({})
        


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def handle_amenity_by_id(amenity_id):
    """Handles GET, DELETE, and PUT requests for a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, "Not a JSON")
        for key, value in req_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
