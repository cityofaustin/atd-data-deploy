# python-docker-cron
Suppose you have a bunch of Python scripts that you'd like to run on a schedule. Suppose you'd like those scripts to run inside Docker containers. Suppose those scripts are transportation-related (that part doesn't really matter).

This tool installs Python scripts as [cron](http://man7.org/linux/man-pages/man8/cron.8.html) jobs that run inside [Docker](https://docs.docker.com/) containers on a Linux host.

## Installation

1. Clone this repo on a Linux host: `git clone https://github.com/cityofaustin/transportation-data-deploy`.

2. Define script and `docker run` parameters in `config/scripts` and `config/docker`.

3. `$ bash build.sh` to generate shell scripts and cron entries.

4. `$ bash deploy.sh` to install crontab on host.

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights of the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
