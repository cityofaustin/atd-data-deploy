# transportation-data-deploy
Run Python scripts with Docker + cron.

### Installation

1. Clone this repo on a Linux server: `git clone https://github.com/cityofaustin/transportation-data-deploy`.

2. Define script parameters in `config.py`.

2. Run `$ bash build.sh` to generate shell scripts and cron entries.

3. Run `$ bash deploy.sh` to install crontab on host.
