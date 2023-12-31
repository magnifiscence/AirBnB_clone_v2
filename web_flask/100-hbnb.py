#!/usr/bin/python3
"""Flask web app."""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User

app = Flask(__name__)


@app.teardown_appcontext
def teardown_context(exception):
    """Close storage when teardown"""
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def hbbnb():
    """List places from db. And populate filters

    Returns:
        template: hbnb template
    """
    states = storage.all(State)
    cities = storage.all(City)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    users = storage.all(User)
    return render_template("100-hbnb.html",
                           states=states,
                           cities=cities,
                           places=places,
                           users=users,
                           amenities=amenities)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)
