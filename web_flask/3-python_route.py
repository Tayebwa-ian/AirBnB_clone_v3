#!/usr/bin/python3
"""Run a flask app Module"""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index() -> str:
    """landing route"""
    return("Hello HBNB!")


@app.route("/hbnb", strict_slashes=False)
def hbnb() -> str:
    """route to hbnb"""
    return("HBNB")


@app.route("/c/<path:text>", strict_slashes=False)
def c_text(text) -> str:
    """display dynamic url values"""
    text = text.replace("_", " ")
    return(f"C {text}")


@app.route("/python/<path:text>", strict_slashes=False)
@app.route("/python/", strict_slashes=False)
@app.route("/python", strict_slashes=False)
def python(text="is cool") -> str:
    """display dynamic url values"""
    text = text.replace("_", " ")
    return(f"Python {text}")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
