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
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        myFile = "versions/web_static_{}.tgz".format(current_time)
        local("tar -cvzf {} web_static".format(myFile))
        return myFile
    except:
        return None
