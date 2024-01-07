#!/usr/bin/python3
"""PLACE REVIEWS"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """GET all reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    reviews_list = [review.to_dict() for review in reviews]
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """GET one review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """DELETE one review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """POST one review"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    if "text" not in request.get_json():
        abort(400, "Missing text")
    user = storage.get(User, request.get_json()["user_id"])
    if user is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review = Review(**request.get_json())
    review.user_id = request.get_json()["user_id"]
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review(review_id):
    """PUT one review"""
    if not request.get_json():
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
