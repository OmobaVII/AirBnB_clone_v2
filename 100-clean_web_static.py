#!/usr/bin/python3
"""
Cleans the older archive from
webservers
"""
from fabric.api import local, run, env, cd
import os

env.hosts = ['18.235.234.111', '100.25.181.230']


def do_clean(number=0):
    """deletes older versions of data from web server"""
    n = 1 if int(number) == 0 else int(number)
    files = [f for f in os.listdir('./versions')]
    files.sort(reverse=True)
    for f in files[n:]:
        local("rm -f versions/{}".format(f))
    remote = "/data/web_static/releases/"
    with cd(remote):
        tgz = run(
            "ls -tr | grep -E '^web_static_([0-9]{6,}){1}$'"
        ).split()
        tgz.sort(reverse=True)
        for d in tgz[n:]:
            run("rm -rf {}{}".format(remote, d))
