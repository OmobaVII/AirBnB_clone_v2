#!/usr/bin/python3
"""
Creates archive and deploys it
"""
from fabric.api import local, run, put, env
from os.path import exists, isdir
from datetime import datetime
from os import stat

env.hosts = ['18.235.234.111', '100.25.181.230']


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


def do_deploy(archive_path):
    """deploy web_static using fabric"""
    if not exists(archive_path):
        flag = False
    try:
        put(archive_path, "/tmp/")
        filename_ext = archive_path.split("/")[-1]
        filename = filename_ext.split(".")[0]
        path = "/data/web_static/releases/"
        full_path = path + filename
        run('mkdir -p {}/'.format(full_path))
        run('tar -xzf /tmp/{} -C {}/'.format(filename_ext, full_path))
        run('rm -rf /tmp/{}'.format(filename_ext))
        run('mv {}/web_static/* {}/'.format(full_path, full_path))
        run('rm -rf {}/web_static'.format(full_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(full_path))
        print("New version deployed!")
        flag = True
    except Exception as e:
        flag = False
    return flag


def deploy():
    """creates and deploys an archive to my servers"""
    archive = do_pack()
    if archive is None:
        return False
    success = do_deploy(archive)
    return success
