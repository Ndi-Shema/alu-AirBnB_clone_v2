#!/usr/bin/python3
"""Importing from better sources"""
from fabric.api import *
import os
import re
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['75.101.238.212', '54.85.162.84']


def do_pack():
    """timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_name = fversions/web_static_{timestamp}.tgz
    local("mkdir -p versions")
    with hide('running'):
        result = local(ftar -czvf {archive_name} web_static/)
    if result.failed:
        return None
    return archive_name


def do_deploy(archive_path):
    """deploying the saved archives"""
    if not os.path.isfile(archive_path):
        return False
    #trying to upload all the archive names to the server
    archive_filename = os.path.splitext(os.path.basename(archive_path))[0]
    archive_remote_path = f/tmp/{archive_filename}.tgz
    try:
        put(archive_path, archive_remote_path)
        run(fmkdir -p /data/web_static/releases/{archive_filename})
        run(ftar -xzf {archive_remote_path} 
            f-C /data/web_static/releases/{archive_filename}/ 
            --strip-components 1)
        run(frm {archive_remote_path})
        run(fmv /data/web_static/releases/{archive_filename}/web_static/* 
            f/data/web_static/releases/{archive_filename}/)
        run(frm -rf /data/web_static/releases/{archive_filename}/web_static)
        run(frm -rf /data/web_static/current)
        run(fln -s /data/web_static/releases/{archive_filename} 
            f/data/web_static/current)
        return True
    except Exception:
        return False
