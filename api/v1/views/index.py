#!/usr/bin/python3
"""
Module contains routes to landing page
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status() -> None:
    """Endpoint returning status of the app"""
    return(jsonify({"status": "OK"}))
