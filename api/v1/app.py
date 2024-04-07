#!/usr/bin/python3
"""
Module contain app instance
And all config necessary to run the app
"""
from flask import Flask, jsonify
from models import storage
from .views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown(self) -> None:
    """Close the storage session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """json 404 page"""
    return(jsonify({"error": "Not found"}))


@app.errorhandler(400)
def handle_bad_request(error):
    """json 400 page"""
    return(jsonify({'error': 'Bad request'}))


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host, port=port, threaded=True, debug=True)
