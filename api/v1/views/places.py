#!/usr/bin/python3
"""
View for Place objects that handles default RestFul API actions
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from api.v1.views import app_views
import requests
import json
from os import getenv


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def handle_places(city_id):
    """Handles GET and POST requests for places under a specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places]), 200
    elif request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, "Not a JSON")
        if 'user_id' not in req_data:
            abort(400, "Missing user_id")
        user = storage.get("User", req_data['user_id'])
        if not user:
            abort(404)
        if 'name' not in req_data:
            abort(400, "Missing name")
        place = Place(**req_data)
        setattr(place, 'city_id', city_id)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place_by_id(place_id):
    """Handles GET, DELETE, and PUT requests for a specific place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return {}, 200
    elif request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, "Not a JSON")
        for key, value in req_data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects based on the JSON in the request body"""
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")

    if not any(key in req_data for key in ('states', 'cities', 'amenities')):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    places = set()

    if 'states' in req_data:
        for state_id in req_data['states']:
            state = storage.get("State", state_id)
            if state:
                places.update(state.cities)

    if 'cities' in req_data:
        for city_id in req_data['cities']:
            city = storage.get("City", city_id)
            if city:
                places.add(city)

    if not places:
        places.update(storage.all(Place).values())

    if 'amenities' in req_data:
        for amenity_id in req_data['amenities']:
            url = "http://0.0.0.0:{}/api/v1/amenities/{}/places".format(
                getenv('HBNB_API_PORT', '5000'), amenity_id)
            response = requests.get(url)
            places.intersection_update(storage.get("Place", place_id) for place_id in json.loads(response.text))

    return jsonify([place.to_dict() for place in places])
