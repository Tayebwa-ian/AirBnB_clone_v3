#!/usr/bin/python3
"""
Module contains all routes to cities
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import City, State, storage


@app_views.route("/states/<state_id>/cities",  methods=['GET', 'POST'])
@app_views.route("/cities/<city_id>",  methods=['GET', 'DELETE', 'PUT'])
def cities(city_id=None, state_id=None):
    """
    city endpoints
        1. retrieve all cities in a specific state
        2. retrieve a single city by id
        3. create a new city
        4. delete a city using and id
        5. Update a city based on id and values
    """
    result = []
    if request.method == "GET":
        if city_id:  # retreive a single city
            city = storage.get(City, city_id)
            if not city:
                abort(404)
            result = city.to_dict()
        elif state_id:  # retrieve all cities related to a specific state
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            cities = state.cities
            for city in cities:
                result.append(city.to_dict())
        return(jsonify(result), 200)
    if request.method == 'DELETE':  # delete a cities from the storage
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        storage.delete(city)
        return(jsonify({}), 200)
    if request.method == 'POST' and state_id:
        # create and add a city to the storage
        state = storage.get(State, state_id)
        try:
            data = request.get_json()
        except Exception as e:
            return(jsonify({"error": "Not a JSON"}), 400)
        try:
            name = data['name']
        except KeyError as e:
            return(jsonify({"error": "Missing name"}), 400)
        city = City(name=name, state_id=state.id)
        city.save()
        return(jsonify(city.to_dict()), 201)
    if request.method == "PUT":  # make changes to existing city
        if city_id:
            city = storage.get(City, city_id)
            if not city:
                abort(404)
            try:
                data = request.get_json()
            except Exception as e:
                return(jsonify({"error": "Not a JSON"}), 400)
            name = data.get('name')
            if name:
                city.name = name
            city.save()
            temp_dict = city.to_dict()
            return(jsonify(temp_dict), 200)
