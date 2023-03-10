#!/usr/bin/python3
# This fabfile is used to deploy an archive to a web server.
import os.path
from fabric.api import env, put, run

# Set hosts to distribute archive
env.hosts = ["75.101.238.212", "54.85.162.84"]


def do_deploy(archive_path):
    """
    Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        True if successful, False otherwise.
    """

    # Check if the archive file exists
    if not os.path.isfile(archive_path):
        return False

    # Extract the archive file name and directory name
    archive_file = archive_path.split("/")[-1]
    name = archive_file.split(".")[0]

    # Upload the archive to the /tmp directory on the web server
    if put(archive_path, "/tmp/{}".format(archive_file)).failed:
        return False

    # Remove any existing release directory and create a new one
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Getting the content of the archive to the directory and remove the archive
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive_file, name)).failed:
        return False
    if run("rm /tmp/{}".format(archive_file)).failed:
        return False

    # Move the contents of the web_static directory to the release directory
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False

    # Remove the web_static directory and create a symbolic link to the new release
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False

    # Return True if successful
    return True
