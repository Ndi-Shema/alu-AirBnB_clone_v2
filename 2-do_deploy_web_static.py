#!/usr/bin/python3
"""Deploying archives to the server"""
import datetime
import os
import shutil
import subprocess

from fabric import Connection


# Server configuration
SERVERS = ['75.101.238.212', '54.85.162.84']
REMOTE_USER = 'ubuntu'
REMOTE_DIR = '/data/web_static'
CURRENT_LINK = os.path.join(REMOTE_DIR, 'current')
BACKUP_DIR = os.path.join(REMOTE_DIR, 'backups')


def do_pack():
    """Create a compressed archive of the web_static directory."""
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    archive_name = f'web_static_{timestamp}.tgz'
    local_dir = os.path.abspath('web_static')
    local_archive = os.path.join(os.path.abspath('versions'), archive_name)

    os.makedirs(os.path.dirname(local_archive), exist_ok=True)

    with subprocess.Popen(
            ['tar', '-czf', local_archive, '-C', local_dir, '.'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
    ) as proc:
        out, err = proc.communicate()

    if proc.returncode != 0:
        print(f'Error creating archive: {err.decode()}')
        return None

    print(f'Created archive: {local_archive}')
    return local_archive


def do_deploy(archive_path):
    """Upload and extract the archive on the remote server."""
    if not os.path.isfile(archive_path):
        print(f'Archive not found: {archive_path}')
        return False

    archive_name = os.path.basename(archive_path)
    remote_archive = os.path.join('/tmp', archive_name)
    c = Connection(REMOTE_USER, SERVERS[0])

    # Create backups directory if it doesn't exist
    c.run(f'mkdir -p {BACKUP_DIR}')

    # Upload archive to remote server
    c.put(archive_path, remote_archive)

    # Extract archive to temporary directory
    temp_dir = os.path.join(REMOTE_DIR, 'tmp')
    c.run(f'mkdir -p {temp_dir}')
    c.run(f'tar -xzf {remote_archive} -C {temp_dir}')

    # Create new release directory and move files
    release_dir = os.path.join(REMOTE_DIR, 'releases', archive_name[:-4])
    c.run(f'mkdir -p {release_dir}')
    c.run(f'mv {temp_dir}/web_static/* {release_dir}')

    # Remove temporary directory and archive
    c.run(f'rm -rf {temp_dir}')
    c.run(f'rm {remote_archive}')

    # Update symbolic link
    c.run(f'rm -f {CURRENT_LINK}')
    c.run(f'ln -s {release_dir} {CURRENT_LINK}')

    print('Deployment successful!')
    return True
