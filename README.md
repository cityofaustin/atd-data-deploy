# transportation-data-deploy
Run Python scripts with [Docker](https://docs.docker.com/) + [cron](http://man7.org/linux/man-pages/man8/cron.8.html).

### Installation

1. Clone this repo on a Linux host: `git clone https://github.com/cityofaustin/transportation-data-deploy`.

2. Define script parameters in `config.py`.

2. Run `$ bash build.sh` to generate shell scripts and cron entries.

3. Run `$ bash deploy.sh` to install crontab on host.
