#!/usr/bin/python3
"""
A Fabric Script that generates a .tgz archive
from the contents of the web_static folder
using a function do_pack
"""
from fabric.api import local
from time import strftime


def do_pack():
    """generates a .tgx archive from web_static"""
    try:
	current_time = strftime("%Y%m%d%H%M%S")
	if isdir("versions") is False:
        	local("mkdir versions")
        myFile = "versions/web_static_{}.tgz".format(current_time)
        local("tar -cvzf {} web_static/".format(myFile))
        return myFile
    except Exception as e:
        return None
