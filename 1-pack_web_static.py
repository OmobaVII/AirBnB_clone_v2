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
        date = "{}{}{}{}".format(datetime.now().year, datetime.now().month,
                                 datetime.now().day, datetime.now().hour,
                                 datetime.now().minute, datetime.now().second)
        myFile = "web_static_{}.tgz".format(date)
        path = "versions/{}".format(myFile)

        if not isdir("versions"):
            if local("mkdir -p versions").failed:
                return None

        if (local("cd web_static && tar -cvzf ../{} . && cd -".format(path))).succeeded:
            return path

        return None
