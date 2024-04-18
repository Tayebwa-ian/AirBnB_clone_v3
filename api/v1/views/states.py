#!/usr/bin/python3
"""
Module contains all routes to states
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import State, storage


@app_views.route("/states",  methods=['GET', 'POST'])
@app_views.route("/states/<state_id>",  methods=['GET', 'DELETE', 'PUT'])
def states(state_id=None):
    """
    State endpoints
        1. retrieve all states
        2. retrieve a single state by id
        3. create a new state
        4. delete a state using and id
        5. Update a state based on id and values
    """
    result = []
    if request.method == "GET":
        if state_id:  # retreive a single state
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            result = state.to_dict()
        else:  # retrieve all states
            states = storage.all(State)
            for key in states.keys():
                result.append(states[key].to_dict())
        return(jsonify(result), 200)
    if request.method == 'DELETE':  # delete a states from the storage
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        storage.delete(state)
        return(jsonify({}), 200)
    if request.method == 'POST':  # create and add a state to the storage
        try:
            data = request.get_json()
        except Exception as e:
            abort(400, "Not a JSON")
        try:
            name = data['name']
        except KeyError as e:
            abort(400, "Missing name")
        state = State(name=name)
        state.save()
        return(jsonify(state.to_dict()), 201)
    if request.method == "PUT":  # make changes to existing state
        if state_id:
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            try:
                data = request.get_json()
            except Exception as e:
                abort(400, "Not a JSON")
            name = data.get('name')
            if name:
                state.name = name
            state.save()
            temp_dict = state.to_dict()
            return(jsonify(temp_dict), 200)
