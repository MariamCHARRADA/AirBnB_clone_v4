#!/usr/bin/python3
""" Index module """
from api.v1.views import app_views
from flask import make_response, json


@app_views.route("/status", methods=["GET"])
def get_status():
    """returns status ok"""
    response_data = {"status": "OK"}
    response_json = json.dumps(response_data)

    response = make_response(response_json)
    response.headers["Content-Type"] = "application/json"

    return response
