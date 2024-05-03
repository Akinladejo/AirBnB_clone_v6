#!/usr/bin/python3
"""places Module"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_in_city(city_id):
    """Retrieves the list of all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place in a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    required_fields = ['user_id', 'name']
    for field in required_fields:
        if field not in request_dict:
            abort(400, f'Missing {field}')
    user_id = request_dict['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    place = Place(**request_dict)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request_dict.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects based on the request JSON"""
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    states = request_dict.get('states', [])
    cities = request_dict.get('cities', [])
    amenities = request_dict.get('amenities', [])

    all_places = []
    places = []

    if not states and not cities:
        all_places = storage.all(Place).values()
    else:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                all_places.extend(place for city in state.cities for place in city.places)
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                all_places.extend(city.places)

    for place in all_places:
        if not amenities or all(amenity_id in place.amenities for amenity_id in amenities):
            places.append(place.to_dict())

    return jsonify(places)
