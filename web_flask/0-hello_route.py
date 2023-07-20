#!/usr/bin/python3
"""
Starts Flask web application
Web app listens on 0.0.0.0 port 5000
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """so the route must display Hello HBNB!"""
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
