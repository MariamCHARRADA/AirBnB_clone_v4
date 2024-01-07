#!/usr/bin/python3
"""AMENITIES"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """GET all amenities"""
    all_amenities = storage.all(Amenity).values()
    all_amenities = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """GET one amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """DELETE one amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """POST one amenity"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """PUT one amenity"""
    if not request.get_json():
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
