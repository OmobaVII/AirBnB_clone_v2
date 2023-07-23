#!/usr/bin/python3
"""
Starts Flask web appliacation
web app listens on 0.0.0.0 port 5000
/cities_by_states page included
"""
from models import *
from models import storage
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    """after each request, remove the current session"""
    storage.close()


@app.route('/cities_by_states')
def cities_by_state():
    """displays a HTML page with the list of cities and the states
    they fall under"""
    sorted_states = [s for s in storage.all("State").values()]
    return render_template('8-cities_by_states.html', states=sorted_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
