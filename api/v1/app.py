#!/usr/bin/python3
"""
Module contain app instance
And all config necessary to run the app
"""
from flask import Flask, jsonify
from models import storage
from .views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self) -> None:
    """Close the storage session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """json 404 page"""
    return(jsonify({"Error": "Page Not Found"}), 404)


if __name__ == "__main__":
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if getenv("HBNB_API_PORT"):
        port = int(getenv("HBNB_API_PORT"))
    else:
        port = 5000
    app.run(host, port=port, threaded=True, debug=True)
