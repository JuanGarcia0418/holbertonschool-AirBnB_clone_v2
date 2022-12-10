#!/usr/bin/python3
"""add flask"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """states_list"""
    state_dict = storage.all(State)
    result = []
    for state in state_dict.values():
        result.append(state)
    return render_template('7-states_list.html', state_list=result)


@app.teardown_appcontext
def teardown_db(self):
    """teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
