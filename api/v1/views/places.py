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
            abort(400, "Not a JSON")
        try:
            name = data['name']
        except KeyError as e:
            abort(400, "Missing name")
        try:
            user_id = data['user_id']
        except KeyError as e:
            abort(400, "Missing user_id")
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
                abort(400, "Not a JSON")
            name = data.get('name')
            description = data.get('description')
            number_rooms = int(data.get('number_rooms'))
            number_bathrooms = int(data.get('number_bathrooms'))
            max_guest = int(data.get('max_guest'))
            price_by_night = float(data.get('latitude'))
            latitude = float(data.get('latitude'))
            longitude = float(data.get('longitude'))
            if name:
                place.name = name
            if description:
                place.description = description
            if number_rooms:
                place.number_rooms = number_rooms
            if number_bathrooms:
                place.number_bathrooms = number_bathrooms
            if max_guest:
                place.max_guest = max_guest
            if price_by_night:
                place.price_by_night = price_by_night
            if latitude:
                place.latitude = latitude
            if longitude:
                place.longitude = longitude
            place.save()
            temp_dict = place.to_dict()
            return(jsonify(temp_dict), 200)
