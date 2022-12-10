#!/usr/bin/python3
"""Flask"""
from flask import Flask, render_template
from models.state import State
from models import storage
app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def states_list():
    """states_list"""
    state_dict = storage.all(State)
    return render_template('8-cities_by_states', state_list=state_dict)


@app.teardown_appcontext
def teardown_db(exception):
    """teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
