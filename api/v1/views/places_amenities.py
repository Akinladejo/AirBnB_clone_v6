#!/usr/bin/python3
"""places_amenities Module"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import abort, jsonify, request


# Route to retrieve all amenities in a place
@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_in_place(place_id):
    """Retrieves the list of all amenities in a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities_list = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities_list)


# Route to delete an amenity from a place
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes an amenity from a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


# Route to link an amenity to a place
@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Links an amenity to a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
