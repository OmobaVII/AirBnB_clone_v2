#!/usr/bin/python3
"""
A Fabric Script that distributes an archive to
my web servers
"""

from fabric.api import run, put, env
from os.path import exists


env.hosts = ['18.235.234.111', '100.25.181.230']


def do_deploy(archive_path):
    """deploy web_static using fabric"""
    if not exists(archive_path):
        return False
    filename_ext = archive_path.split("/")[-1]
    filename = filename_ext.split(".")[0]
    full_path = "/data/web_static/releases/{}".format(filename)
    if put(archive_path, "/tmp/").failed:
        return False
    if run("mkdir -p {}".format(full_path)).failed:
        return False
    if run("tar -xzf /tmp/{} -C {}/".format(filename_ext, full_path)).failed:
        return False
    if run("rm /tmp/{}".format(filename_ext)).failed:
        return False
    if run("mv {}/web_static/* {}/".format(full_path, full_path)).failed:
        return False
    if run("rm -rf {}/web_static".format(full_path)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s {} /data/web_static/current".format(full_path)).failed:
        return False
    return True
