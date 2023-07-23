#!/usr/bin/python3
"""
Starts Flask web application
Web app listens on 0.0.0.0 port 5000
/hbnb page include
/c/<text> page included
/python/(<text>) page included
/number/<n> page included
/number_template/<n> page included
/number_odd_or_even/<n> page included
"""
from models import storage
from models import *
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """so the route must display Hello HBNB!"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """so the route must display HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def custom_text(text):
    """so the route must display c + text"""
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """so the route must display python + text"""
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """so the route must display n is a number"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """so the route must display the number template"""
    if isinstance(n, int):
        return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """so the route must display odd or even template"""
    if isinstance(n, int):
        if n % 2 == 0:
            flag = "even"
        else:
            flag = "odd"
        return render_template('6-number_odd_or_even.html', n=n, flag=flag)


@app.teardown_appcontext
def teardown_db(self):
    """After each request, remove the current session"""
    storage.close()


@app.route('/states_list')
def states_list():
    """displays a HTML page with the list of all
    states objects"""
    sorted_states = [s for s in storage.all("State").values()]

    return render_template('7-states_list.html', states=sorted_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
