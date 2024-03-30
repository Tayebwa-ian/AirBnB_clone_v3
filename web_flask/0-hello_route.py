#!/usr/bin/python3
"""Run a flask app Module"""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index() -> str:
    """landing route"""
    return("Hello HBNB!")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
