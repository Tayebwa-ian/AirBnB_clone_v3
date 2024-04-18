#!/usr/bin/python3
"""
Module contains all routes to users
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import User, storage
import hashlib

hash_object = hashlib.md5()


@app_views.route("/users",  methods=['GET', 'POST'])
@app_views.route("/users/<user_id>",  methods=['GET', 'DELETE', 'PUT'])
def users(user_id=None):
    """
    user endpoints
        1. retrieve all users
        2. retrieve a single user by id
        3. create a new user
        4. delete a user using and id
        5. Update a user based on id and values
    """
    result = []
    if request.method == "GET":
        if user_id:  # retreive a single user
            user = storage.get(User, user_id)
            if not user:
                abort(404)
            result = user.to_dict()
        else:  # retrieve all users
            users = storage.all(User)
            for key in users.keys():
                result.append(users[key].to_dict())
        return(jsonify(result), 200)
    if request.method == 'DELETE':  # delete a users from the storage
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        storage.delete(user)
        return(jsonify({}), 200)
    if request.method == 'POST':  # create and add a user to the storage
        try:
            data = request.get_json()
        except Exception as e:
            abort(400, "Not a JSON")
        try:
            email = data['email']
        except KeyError as e:
            abort(400, "Missing email")
        try:
            password = data['password']
            hash_object.update(password.encode())
            password = hash_object.hexdigest()
        except KeyError as e:
            abort(400, "Missing password")
        user = User(email=email, password=password)
        user.save()
        return(jsonify(user.to_dict()), 201)
    if request.method == "PUT":  # make changes to existing user
        if user_id:
            user = storage.get(User, user_id)
            if not user:
                abort(404)
            try:
                data = request.get_json()
            except Exception as e:
                abort(400, "Not a JSON")
            password = data.get('password')
            name = data.get('name')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            if password:
                hash_object.update(password.encode())
                password = hash_object.hexdigest()
                user.password = password
            if name:
                user.name = name
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()
            temp_dict = user.to_dict()
            return(jsonify(temp_dict), 200)
