#!/usr/bin/python3
"""
Module contains all routes to amenities
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import Amenity, storage


@app_views.route("/amenities",  methods=['GET', 'POST'])
@app_views.route("/amenities/<amenity_id>",  methods=['GET', 'DELETE', 'PUT'])
def amenitys(amenity_id=None):
    """
    amenity endpoints
        1. retrieve all amenities
        2. retrieve a single amenity by id
        3. create a new amenity
        4. delete a amenity using and id
        5. Update a amenity based on id and values
    """
    result = []
    if request.method == "GET":
        if amenity_id:  # retreive a single amenity
            amenity = storage.get(Amenity, amenity_id)
            if not amenity:
                abort(404)
            result = amenity.to_dict()
        else:  # retrieve all amenitys
            amenities = storage.all(Amenity)
            for key in amenities.keys():
                result.append(amenities[key].to_dict())
        return(jsonify(result), 200)
    if request.method == 'DELETE':  # delete a amenitys from the storage
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        storage.delete(amenity)
        return(jsonify({}), 200)
    if request.method == 'POST':  # create and add a amenity to the storage
        try:
            data = request.get_json()
        except Exception as e:
            abort(400, "Not a JSON")
        try:
            name = data['name']
        except KeyError as e:
            abort(400, "Missing name")
        amenity = Amenity(name=name)
        amenity.save()
        return(jsonify(amenity.to_dict()), 201)
    if request.method == "PUT":  # make changes to existing amenity
        if amenity_id:
            amenity = storage.get(Amenity, amenity_id)
            if not amenity:
                abort(404)
            try:
                data = request.get_json()
            except Exception as e:
                abort(400, 'Not a JSON')
            name = data.get('name')
            if name:
                amenity.name = name
            amenity.save()
            temp_dict = amenity.to_dict()
            return(jsonify(temp_dict), 200)
