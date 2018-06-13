"""
Generate shell scripts config and crontab for deployment.
"""
import os
import pdb
import sys

from config import CONFIG
from config import CRONTAB
from config import DOCKER_BASE_CMD


def check_version():
    """
    Check system python version and raise exception if <2.7
    """
    if sys.version_info[0] < 2:
        raise Exception("Python v2.7+ is required")

    elif sys.version_info[0] == 2 and sys.version_info[1] < 7:
        raise Exception("Python v2.7+ is required")

    return


def shell_script(build_path, path, script, args, image):
    """
    Build a shell script which will launch python script in Docker container
    """
    cmd = "cd {}; python {} {}".format(path, script, " ".join(args))

    return (
        DOCKER_BASE_CMD.replace("$BUILD_PATH", build_path)
        .replace("$IMAGE", image)
        .replace("$CMD", cmd)
    )


def cron_entry(cron, path):
    return "{} bash {}".format(cron, path)


def list_to_file(filename, list_, write_mode="a", header=None):
    with open(filename, write_mode) as fout:
        if header:
            fout.write(header)

        for l in list_:
            fout.write(l)
            fout.write("\n")

        #  terminate file with empty line
        #  this is for crontab
        fout.write("\n")
    return


if __name__ == "__main__":
    check_version()

    crontab_filename = "crontab.sh"

    build_path = os.getcwd()
    parent_path = os.path.dirname(os.getcwd())

    crons = []

    for script in CONFIG["scripts"]:

        if not script["enabled"]:
            continue

        if not script.get("image"):
            script["image"] = CONFIG["default_image"]

        sh = shell_script(
            parent_path,
            script["path"],
            script["script"],
            script["args"],
            script["image"],
        )

        sh_filename = "{}/scripts/{}.sh".format(build_path, script["name"])

        list_to_file(sh_filename, [], header=sh, write_mode="w")

        cron = cron_entry(script["cron"], sh_filename)

        crons.append(cron)

    list_to_file(crontab_filename, crons, header=CRONTAB, write_mode="w")
