#!/usr/bin/python3
"""
A Fabric Script that distributes an archive to
my web servers
"""

from fabric.api import run, put, env
from os.path import exists


env.user = "ubuntu"
env.hosts = ['18.235.234.111', '100.25.181.230']


def do_deploy(archive_path):
    """deploy web_static using fabric"""
    if not exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        filename_ext = archive_path.split("/")[-1]
        filename = filename_ext.split(".")[0]
        full_path = "/data/web_static/releases/{}".format(filename)
        run("sudo mkdir -p {}".format(full_path))
        run("sudo tar -xzf /tmp/{} -C {}/".format(filename_ext, full_path))
        run("sudo rm /tmp/{}".format(filename_ext))
        run("sudo mv {}/web_static/* {}/".format(full_path, full_path))
        run("sudo rm -rf {}/web_static".format(full_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(full_path))
        return True
    except BaseException:
        return False
