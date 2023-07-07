#!/usr/bin/python3
"""
Cleans the older archive from
webservers
"""
from fabric.api import local, run, put, env, runs_once
from os.path import exists, isdir
from datetime import datetime

env.hosts = ['18.235.234.111', '100.25.181.230']


def do_clean(number=0):
    """deletes older versions of data from web server"""
    if int(number) == 0:
        flag = 1
    else:
        flag = int(number)
    files = [fil for fil in os.listdir('./versions')]
    files.sort(reverse=True)
    for fil in files[flag:]:
        local("rm -f versions/{}".format(fil))
    origin = "/data/web_static/releases/"
    with cd(origin):
        tgz = run("ls -tr | grep -E '^web_static_([0-9]{6,}){1}$'").split()
        tgz.sort(reverse=True)
        for di in tgz[flag:]:
            run("rm -rf {}{}".format(remote, di))
