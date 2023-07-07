#!/usr/bin/python3
"""
A Fabric Script that generates a .tgz archive
from the contents of the web_static folder
using a function do_pack
"""

from fabric.api import local, run, sudo
from datetime import datetime
from os.path import isdir
from os import stat

date = datetime.now()


def do_pack():
    """generates a .tgx archive from web_static"""
    path = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            date.year, date.month, date.day, date.hour,
            date.minute, date.second)
    local("mkdir -p versions")
    print("Packing web_static to {}".format(path))
    pack = local("tar -cvzf " + path + " ./web_static")
    file_size = stat(path).st_size
    print("web_static packed: {} -> {} Bytes".format(path, file_size))
    if pack.succeeded:
        return path
    return None
