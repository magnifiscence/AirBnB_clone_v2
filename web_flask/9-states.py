#!/usr/bin/python3
"""Starts a Flash Web Application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.teardown_appcontext
def teardown_context(exception):
    """Close storage when teardown"""
    storage.close()


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def state_id(id=None):
    """get state by id

    Returns:
        template: state template
    """
    states = storage.all(State)
    cities = storage.all(City)
    return render_template("9-states.html",
                           states=states, cities=cities, id=id)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)
