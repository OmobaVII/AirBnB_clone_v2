#!/usr/bin/python3
"""
Starts Flask web application
Web app listens on 0.0.0.0 port 5000
/hbnb page include
/c/<text> page included
/python/(<text>) page included
/number/<n> page included
"""
from flask import Flask
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
    """n is a number"""
    return "{:d} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
