#!/usr/bin/python3
import os.path
from fabric import Connection

env.hosts = ["75.101.238.212", "54.85.162.84"]


def do_deploy(archive_path): 
  """deploying archives to the server."""
  
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    with Connection(env.hosts[0]) as conn:
        put_result = conn.put(archive_path, "/tmp/{}".format(file))
        if put_result.failed is True:
            return False

        if conn.run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
            return False
        if conn.run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
            return False
        if conn.run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
            return False
        if conn.run("rm /tmp/{}".format(file)).failed is True:
            return False
        if conn.run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
            return False
        if conn.run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
            return False
        if conn.run("rm -rf /data/web_static/current").failed is True:
            return False
        if conn.run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
            return False
        return True
