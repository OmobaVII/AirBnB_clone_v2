#!/usr/bin/python3
"""
Starts Flask web application
Web app listens on 0.0.0.0 port 5000
/states_list page included
"""
from models import *
from models.state import State
from flask import Flask, render_template
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    """After each request, remove the current session"""
    storage.close()

@app.route('/states_list')
def states_list():
    """displays a HTML page with the list of all
    states objects"""
    sorted_states = [s for s in storage.all(State).values()]

    return render_template('7-state_list.html', states=sorted_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
