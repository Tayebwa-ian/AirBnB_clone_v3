#!/usr/bin/python3
"""
Module contains routes to landing page
"""
from api.v1.views import app_views
from flask import jsonify
from models import User, State, Review, Place, City, Amenity, storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """Endpoint returning status of the app"""
    return(jsonify({"status": "OK"}))

@app_views.route("/stats")
def stats():
    """
    Return number of objects in the storage
    Corresponding to the number of classes
    """
    classes = {
        "users": User,
        "states": State,
        "reviews": Review,
        "places": Place,
        "cities": City,
        "amenities": Amenity,
        }
    result = {}
    for key in classes.keys():
        count = storage.count(classes[key])
        result[key] = count
    return(jsonify(result))
