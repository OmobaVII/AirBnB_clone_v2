#!/usr/bin/python3
"""
Cleans the older archive from
webservers
"""
from fabric.api import local, run, put, env, runs_once
import os

env.hosts = ['18.235.234.111', '100.25.181.230']


def do_clean(number=0):
    """deletes older versions of data from web server"""
    flag = 1 if int(number) == 0 else int(number)
    files = [fil for fil in os.listdir('./versions')]
    files.sort(reverse=True)
    for fil in files[flag:]:
        local("rm -f versions/{}".format(fil))
    origin = "/data/web_static/releases/"
    with cd(origin):
        tgz = run("ls -tr | grep -E '^web_static_([0-9]{6,}){1}$'").split()
        tgz.sort(reverse=True)
        for di in tgz[flag:]:
            run("rm -rf {}{}".format(origin, di))
