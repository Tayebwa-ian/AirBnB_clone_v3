#!/usr/bin/python3
"""
Module contains all routes to reviews
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import Place, Review, storage


@app_views.route("/reviews/<place_id>/reviews",  methods=['GET', 'POST'])
@app_views.route("/reviews/<review_id>",  methods=['GET', 'DELETE', 'PUT'])
def reviews(review_id=None, place_id=None):
    """
    review endpoints
        1. retrieve all reviews in a specific review
        2. retrieve a single review by id
        3. create a new review
        4. delete a review using and id
        5. Update a review based on id and values
    """
    result = []
    if request.method == "GET":
        if review_id:  # retreive a single review
            review = storage.get(Review, review_id)
            if not review:
                abort(404)
            result = review.to_dict()
        elif place_id:  # retrieve all reviews related to a specific review
            place = storage.get(Place, place_id)
            if not place:
                abort(404)
            reviews = place.reviews
            for review in reviews:
                result.append(review.to_dict())
        return(jsonify(result), 200)
    if request.method == 'DELETE':  # delete a reviews from the storage
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        storage.delete(review)
        return(jsonify({}), 200)
    if request.method == 'POST' and place_id:
        # create and add a review to the storage
        place = storage.get(Place, place_id)
        try:
            data = request.get_json()
        except Exception as e:
            abort(400, "Not a JSON")
        try:
            text = data['text']
        except KeyError as e:
            abort(400, "Missing name")
        try:
            user_id = data['user_id']
        except KeyError as e:
            abort(400, "Missing user_id")
        review = Review(text=text, place_id=place.id, user_id=user_id)
        review.save()
        return(jsonify(review.to_dict()), 201)
    if request.method == "PUT":  # make changes to existing review
        if review_id:
            review = storage.get(Review, review_id)
            if not review:
                abort(404)
            try:
                data = request.get_json()
            except Exception as e:
                abort(400, "Not a JSON")
            text = data.get('text')
            if text:
                review.text = text
            review.save()
            temp_dict = review.to_dict()
            return(jsonify(temp_dict), 200)
