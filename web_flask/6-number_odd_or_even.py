#!/usr/bin/python3
"""Run a flask app Module"""
from flask import Flask, render_template


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


@app.route("/number/<int:n>", strict_slashes=False)
def number(n: int) -> str:
    """Take a number value and return string"""
    return(f"{n} is a number")


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n: int):
    """return a dynamic value within a template
    parameter:
        n: the dynamic integer to return in a template
    Return: a template
    """
    return(render_template("5-number.html", number=n))


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n: int):
    """return a dynamic value within a template
    parameter:
        n: the dynamic integer to return in a template
    Return: a template
    """
    return(render_template("6-number_odd_or_even.html", number=n))


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
