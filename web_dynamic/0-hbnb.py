#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /hbnb: HBnB home page.
"""
from models import *
from flask import Flask
from flask import render_template
import uuid

app = Flask(__name__)


@app.route("/0-hbnb/", strict_slashes=False)
def hbnb():
    """Displays the main HBnB filters HTML page."""
    cache_id = str(uuid.uuid4())
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    users = storage.all(User).values()
    return render_template("0-hbnb.html",
                           states=states, cache_id=cache_id,
                           amenities=amenities, places=places,
                           users=users)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
