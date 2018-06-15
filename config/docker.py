"""
Configuration file for Docker commands.

Each DOCKER entry specifies a `docker run` command that will be generated via `build.py`.

Entries are referenced by Python scripts defined in `config/scripts`. The first entry
must be named `default`. Contents are defined as follows:

    - options: `docker run` options as defined here: https://docs.docker.com/engine/reference/commandline/run/ | optional
    - image: name of the Docker image to run | required
    - command: the base command that will be run by the Docker container | optional
    - args:  args to be appened to the base command. Typically this would include the
        name of the python | options

Entries support three magical vars which are replaced at build time with
    parameters from the SCRIPTS configuration:
- $BUILD_PATH: The absolute path to the parent directory of this repository.
    Presuming this repository shares a parent directory with the script source files,
    this makes it possible to properly mount the scripting directory regardless of the
    host file structure. See "workdir" element of the SCRIPTS configuration
- $CMD: This is the means by which a Python scripts defined in SCRIPTS is run by the
    docker container. $CMD will be replaced with the python script name and command
    arguments definedin SCRIPTS.
- $WORKDIR: The relative path defined in SCRIPTS.
"""

DOCKER = {
    "default": {
        "options": ["-d", "-v $BUILD_PATH:/app", "--rm", "--network=host", "-w /app/$WORKDIR"],
        "image": "atddocker/tdp",
        "command": "python",
        "args": ["$CMD"],
    },
    "test": {
        "options": ["-v $BUILD_PATH:/app", "--rm", "--network=host", "-w /app/$WORKDIR"],
        "image": "atddocker/tdp",
        "command": "python",
        "args": ["$CMD"],
    }
}













