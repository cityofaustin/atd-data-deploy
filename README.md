# transportation-data-deploy

This repository houses a deployment framework for Austin Transportation's ETL scripting tasks. It uses [Python](https://www.python.org/download/releases/3.0/), [Docker](https://docs.docker.com/) and [cron](http://man7.org/linux/man-pages/man8/cron.8.html) to schedule and monitor each task. The framework's core components are:

#### Launcher (launch.py)

The launcher acts as a wrapper for each ETL script and manages logging, email notifications, and job registration for incremental data loading.

#### Builder (build.sh)
    
The builder generates a `docker run` command for each task. It ensures each task is properly passed to **launcher**, and packages it as a shell script which can be installed as a cron job.

#### Deployer (deploy.sh)
    
Given the master task list, the deployer schedules each script by installing a crontab on a Linux host.


## Installation

1. Clone this repo on a Linux host: `git clone https://github.com/cityofaustin/transportation-data-deploy`.

2. Define script and `docker run` parameters in `config/scripts.yml` and `config/docker.yml` respectively.

3. `$ bash build.sh` to generate shell scripts and cron entries.

4. `$ bash deploy.sh` to install crontab on host.

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights of the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
