#!/usr/bin/env python3
"""Comment"""
import os
import re
from datetime import datetime
from fabric import Connection
from invoke import Responder

env.user = 'ubuntu'
env.hosts = ['3.80.74.138', '3.88.68.105']


def do_pack():
    """Comm"""
    local("mkdir -p versions")
    result = local("tar -cvzf versions/web_static_{}.tgz web_static"
                   .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                   capture=True)
    if result.failed:
        return None
    return result


def do_deploy(archive_path):
    """Comment"""
    if not os.path.isfile(archive_path):
        return False

    filename_regex = re.compile(r'[^/]+(?=\.tgz$)')
    match = filename_regex.search(archive_path)

    # Upload the archive to the /tmp/ directory of the web server
    archive_filename = match.group(0)
    remote_path = "/tmp/{}.tgz".format(archive_filename)
    c = Connection(host=env.hosts[0], user=env.user)
    c.put(archive_path, remote=remote_path)

    # Uncompress the archive to the folder
    #     /data/web_static/releases/<archive filename without extension> on
    #     the web server
    remote_dir = "/data/web_static/releases/{}/".format(archive_filename)
    c.run("sudo mkdir -p {}".format(remote_dir))
    c.run("sudo tar -xzf {} -C {} --strip-components=1".format(remote_path, remote_dir))

    # Delete the archive from the web server
    c.run("sudo rm {}".format(remote_path))

    # Move the contents of web_static to the new folder
    c.run("sudo mv {} /data/web_static/releases/{}/".format(remote_dir + "web_static/*", archive_filename))

    # Remove the old symbolic link and create a new one
    c.run("sudo rm -rf /data/web_static/current")
    c.run("sudo ln -s {} /data/web_static/current".format(remote_dir))

    return True
