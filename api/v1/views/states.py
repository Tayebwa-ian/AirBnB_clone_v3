#!/usr/bin/python3
"""
Module contains all routes to states
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import State, storage


@app_views.route("/states",  methods=['GET', 'POST'])
@app_views.route("/states/<str:state_id>",  methods=['GET', 'DELETE', 'PUT'])
def states(state_id):
    """
    State endpoints
        1. retrieve all states
        2. retrieve a single state by id
        3. create a new state
        4. delete a state using and id
        5. Update a state based on id and values
    """
    result = {}
    if request.method == "GET":
        if state_id:
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            result = state.to_dict()
        else:
            states = storage.all(State)
            for key in states.keys():
                result[key] = states[key].to_dict()
        return(jsonify(result), 200)
    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        storage.delete(state)
        return(jsonify(result), 200)
    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception as e:
            return(jsonify({"error": "Not a JSON"}), 400)
        try:
            name = data['name']
        except KeyError as e:
            return(jsonify({"error": "Missing name"}), 400)
        state = State(name=name)
        state.save()
        return(jsonify(state.to_dict()))
    if request.method == "PUT":
        if state_id:
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            try:
                data = request.get_json()
            except Exception as e:
                return(jsonify({"error": "Not a JSON"}), 400)
            try:
                name = data['name']
            except KeyError as e:
                return(jsonify({"error": "Missing name"}), 400)
            temp_dict = state.to_dict()
            temp_dict['name'] = name
            updated_state = State(**temp_dict)
            return(jsonify(updated_state.to_dict()))
