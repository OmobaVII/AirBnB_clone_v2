#!/usr/bin/python3
"""
A Fabric Script that generates a .tgz archive
from the contents of the web_static folder
using a function do_pack
"""

from fabric.api import local
from datetime import datetime
from os.path import isdir


def do_pack():
    """generates a .tgx archive from web_static"""
    date = "{}{}{}{}".format(datetime.now().year, datetime.now().month,
                             datetime.now().day, datetime.now().hour,
                             datetime.now().minute, datetime.now().second)
    myFile = "web_static_{}.tgz".format(date)

    try:
        if not isdir("versions"):
            local("mkdir -p versions")
        path = "versions/{}".format(myFile)
        local("tar -cvzf {} web_static/".format(path))

        return path
    except Exception:
        return None
