#!/usr/bin/python3
import os
import datetime
from fabric import Connection
from invoke import Responder

env = {'hosts': ['75.101.238.212', '54.85.162.84'], 'user': 'ubuntu', 'key_filename': '~/.ssh/id_rsa'}

def do_pack():
    """
    Compress the web_static folder and save the archive
    in the versions folder with a timestamp.
    """
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"web_static_{now}.tgz"
    os.system("mkdir -p versions")
    os.system(f"tar -czvf versions/{filename} web_static/")
    return f"versions/{filename}"

def do_deploy(archive_path):
    """
    Distribute the archive to the web servers.
    """
    if not os.path.isfile(archive_path):
        return False

    # Upload archive to remote server
    with Connection(env.hosts[0], user=env['user'], connect_kwargs={"key_filename": env['key_filename']}) as conn:
        put_result = conn.put(archive_path, "/tmp/")
        if put_result.failed:
            return False

    # Create remote directory to store the files
    with Connection(env.hosts[0], user=env['user'], connect_kwargs={"key_filename": env['key_filename']}) as conn:
        name = archive_path.split("/")[-1].split(".")[0]
        remote_path = f"/data/web_static/releases/{name}"
        if conn.run(f"mkdir -p {remote_path}").failed:
            return False

    # Extract files from the archive
    with Connection(env.hosts[0], user=env['user'], connect_kwargs={"key_filename": env['key_filename']}) as conn:
        if conn.run(f"tar -xzf /tmp/{name}.tgz -C {remote_path}").failed:
            return False

    # Delete archive from the remote server
    with Connection(env.hosts[0], user=env['user'], connect_kwargs={"key_filename": env['key_filename']}) as conn:
        if conn.run(f"rm /tmp/{name}.tgz").failed:
            return False

    # Move files to the final location
    with Connection(env.hosts[0], user=env['user'], connect_kwargs={"key_filename": env['key_filename']}) as conn:
        if conn.run(f"mv {remote_path}/web_static/* {remote_path}").failed:
            return False

    # Remove old symlink
    with Connection(env.hosts[0], user=env['user'], connect_kwargs={"key_filename": env['key_filename']}) as conn:
        if conn.run(f"rm -rf /data/web_static/current").failed:
            return False

    # Create new symlink
    with Connection(env.hosts[0], user=env['user'], connect_kwargs={"key_filename": env['key_filename']}) as conn:
        if conn.run(f"ln -s {remote_path} /data/web_static/current").failed:
            return False

    return True
