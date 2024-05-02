#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir
import tarfile


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        with tarfile.open(file_name, "w:gz") as tar:
            tar.add("web_static", arcname=".")
        return file_name
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
