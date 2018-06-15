# transportation-data-deploy
Run Python scripts with [Docker](https://docs.docker.com/) + [cron](http://man7.org/linux/man-pages/man8/cron.8.html).

## Installation

1. Clone this repo on a Linux host: `git clone https://github.com/cityofaustin/transportation-data-deploy`.

2. Define script parameters in `config.py`.

2. `$ bash build.sh` to generate shell scripts and cron entries.

3. `$ bash deploy.sh` to install crontab on host.

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights of the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
