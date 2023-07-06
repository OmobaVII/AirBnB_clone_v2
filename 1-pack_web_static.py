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
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        myFile = "web_static_{}.tgz".format(date)
        path = "versions/{}".format(myFile)

        if not isdir("versions"):
            local("mkdir -p versions")

        local("tar -cvzf {} web_static".format(path))

        return path
    except Exception as e:
        return None
