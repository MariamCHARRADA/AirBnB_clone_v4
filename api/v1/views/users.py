#!/usr/bin/python3
"""USERS"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """GET all users"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """GET one user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """DELETE one user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """POST one user"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """PUT one user"""
    if not request.get_json():
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
