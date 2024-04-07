#!/usr/bin/python3
"""
Module contains all routes to places
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import City, Place, storage, Amenity, State


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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return(jsonify(places))
