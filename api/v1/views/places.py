#!/usr/bin/python3
"""PLACES"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/places/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """GET all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """GET one place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """DELETE one place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """POST one place"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    user = storage.get(User, request.get_json()["user_id"])
    if user is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = Place(**request.get_json())
    place.user_id = request.get_json()["user_id"]
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """PUT one place"""
    if not request.get_json():
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
