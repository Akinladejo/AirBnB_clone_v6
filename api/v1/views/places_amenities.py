#!/usr/bin/python3
"""
View for the link between Place and Amenity Review
objects that handles default API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def places_amenities(place_id):
    """ Retrieves the list of all Amenities objects in a Place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        l = [amenity.to_dict() for amenity in place.amenities]
    else:
        l = [storage.get("Amenity", id).to_dict() for id in place.amenity_ids]
    return jsonify(l)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def del_places_amenities(place_id, amenity_id):
    """ Deletes an Amenity object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        index = place.amenity_ids.index(amenity_id)
        place.amenity_ids.pop(index)

    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """ Links an Amenity and a Place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/places/<place_id>/amenities', methods=['POST'], strict_slashes=False)
@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def handle_places_amenities(place_id, amenity_id=None):
    """
    Retrieves the list of all Amenity objects of a Place,
    delete or create an Amenity object of a Place
    """
    place_obj = storage.get("Place", place_id)
    if place_obj:
        if request.method == 'GET' and amenity_id is None:
            return jsonify([amenity_obj.to_dict() for amenity_obj in place_obj.amenities]), 200
        amenity_ids = [amenity_obj.id for amenity_obj in place_obj.amenities]
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj:
            if request.method == 'DELETE':
                if amenity_id not in amenity_ids:
                    abort(404)
                place_obj.amenities.remove(amenity_obj)
                storage.save()
                return {}, 200
            if request.method == 'POST':
                if amenity_id in amenity_ids:
                    return jsonify(amenity_obj.to_dict()), 200
                place_obj.amenities.append(amenity_obj)
                place_obj.save()
                return jsonify(amenity_obj.to_dict()), 201
        else:
            abort(404)
    else:
        abort(404)
