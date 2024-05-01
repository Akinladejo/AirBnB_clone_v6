#!/usr/bin/python3
"""
View for City objects that handles default RestFul API actions
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from api.v1.views import app_views
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def handle_cities(state_id):
    """Handles GET and POST requests for cities under a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities]), 200
    elif request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, "Not a JSON")
        if 'name' not in req_data:
            abort(400, "Missing name")
        city = City(**req_data)
        setattr(city, 'state_id', state_id)
        storage.new(city)
        storage.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city_by_id(city_id):
    """Handles GET, DELETE, and PUT requests for a specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, "Not a JSON")
        for key, value in req_data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
