#!/usr/bin/python3
"""
Cleans the older archive from
webservers
"""
from fabric.api import local, run, put, env, runs_once
from os.path import exists, isdir
from datetime import datetime
from os import stat, unlink, listdir

env.hosts = ['18.235.234.111', '100.25.181.230']


@runs_once
def do_pack():
    """generates a .tgx archive from web_static"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir -p versions")
        path = "versions/web_static_{}.tgz".format(date)
        print("Packing web_static to {}".format(path))
        local("tar -cvzf {} web_static".format(path))
        file_size = stat(path).st_size
        print("web_static packed: {} -> {} Bytes".format(path, file_size))
    except Exception:
        path = None
    return path


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
    return do_deploy(archive)

def do_clean(number=0):
    """deletes older versions of data from web server"""
    all_archive = os.listdir('versions/')
    all_archive.reverse()
    begin = int(number)
    if not begin:
        begin = begin + 1
    if begin < len(all_archive):
        all_archive = all_archive[begin:]
    else:
        all_archive = []
    for archive in all_archive:
        os.unlink('versions/{}'.format(archive))
    cmd = ["rm -rf $(",
           "find //data/web_static/releases/ -maxdepth 1 -type d -iregex",
           " '/data/web_static/releases/web_static_.*'",
           " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
           ]
    run("".join(cmd))
