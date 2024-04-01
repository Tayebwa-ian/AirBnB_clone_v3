#!/usr/bin/python3
"""
Module contains all routes to places
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import City, Place, storage


@app_views.route("/places/<city_id>/places",  methods=['GET', 'POST'])
@app_views.route("/places/<place_id>",  methods=['GET', 'DELETE', 'PUT'])
def places(place_id=None, city_id=None):
    """
    place endpoints
        1. retrieve all places in a specific place
        2. retrieve a single place by id
        3. create a new place
        4. delete a place using and id
        5. Update a place based on id and values
    """
    result = []
    if request.method == "GET":
        if place_id:  # retreive a single place
            place = storage.get(Place, place_id)
            if not place:
                abort(404)
            result = place.to_dict()
        elif city_id:  # retrieve all places related to a specific place
            city = storage.get(City, city_id)
            if not city:
                abort(404)
            places = city.places
            for place in places:
                result.append(place.to_dict())
        return(jsonify(result), 200)
    if request.method == 'DELETE':  # delete a places from the storage
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        storage.delete(place)
        return(jsonify({}), 200)
    if request.method == 'POST' and city_id:
        # create and add a place to the storage
        city = storage.get(City, city_id)
        try:
            data = request.get_json()
        except Exception as e:
            return(jsonify({"error": "Not a JSON"}), 400)
        try:
            name = data['name']
        except KeyError as e:
            return(jsonify({"error": "Missing name"}), 400)
        try:
            user_id = data['user_id']
        except KeyError as e:
            return(jsonify({"error": "Missing user_id"}), 400)
        place = Place(name=name, city_id=city.id, user_id=user_id)
        place.save()
        return(jsonify(place.to_dict()), 201)
    if request.method == "PUT":  # make changes to existing place
        if place_id:
            place = storage.get(Place, place_id)
            if not place:
                abort(404)
            try:
                data = request.get_json()
            except Exception as e:
                return(jsonify({"error": "Not a JSON"}), 400)
            name = data.get('name')
            description = data.get('description')
            if name:
                place.name = name
            if description:
                place.description = description
            place.save()
            temp_dict = place.to_dict()
            return(jsonify(temp_dict), 200)
