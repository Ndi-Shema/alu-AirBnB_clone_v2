#!/usr/bin/python3

"""Importing from different sources"""

import os
from fabric.api import local
from datetime import datetime


def do_pack():
    """Packs web_static files in a tgz archive."""
    if not os.path.isdir("versions"):
        os.makedirs("versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    command = "tar -cvzf {} web_static".format(archive_path)
    result = local(command)

    if result.failed:
        return None
    else:
        return archive_path
