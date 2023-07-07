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
    all_archive = os.listdir('versions/')
    all_archive.sort(reverse=True)
    begin = int(number)
    if not begin:
        begin = begin + 1
    if begin < len(all_archive):
        all_archive = all_archive[begin:]
    else:
        all_archive = []
    for archive in all_archive:
        os.unlink('versions/{}'.format(archive))
    cmd = [
            "rm -rf $(",
            "find //data/web_static/releases/ -maxdepth 1 -type d -iregex",
            " '/data/web_static/releases/web_static_.*'",
            " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run("".join(cmd))
