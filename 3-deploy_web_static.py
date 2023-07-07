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
    path = "versions/web_static_{}.tgz".format(
            date.strftime("%Y%m%d%H%M%S"))
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
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}/'.format(path, no_ext))
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))
        run('sudo rm /tmp/{}'.format(file_name))
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('sudo rm -rf {}{}/web_static'.format(path, no_ext))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
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
