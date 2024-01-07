#!/usr/bin/python3
""" Index module """
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=["GET"])
def get_status():
    """returns status ok"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def get_stats():
    """returns number of each objects"""
    from models import storage

    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(stats)
