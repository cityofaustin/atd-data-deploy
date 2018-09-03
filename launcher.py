"""Summary
a script launcher tha handls:
    job creation for job server
    log start and end time
    log exceptions
    dynamically import 
"""
# system packages
import argparse
import importlib
import os
import traceback

import pdb
import sys
import yaml

# other packages
import arrow

# tdutils subpackages
from tdutils import jobutil
from tdutils import emailutil
from tdutils import logutil
from config import secrets


class Script:
    
    def __init__(
        self,
        name,
        log_path = './log',
        config_path='./config/scripts.yml',
    ):

        # set init attributes
        self.name = name
        self.log_path = log_path
        self.config_path = config_path

        # get config and set attributes
        self.config = self._get_config()
        self.args = self.config.get('args')    
        self.dirname = self.config.get('path')
        self.emails = self.config.get('emails')
        self.filename = self.config.get('filename')
        self.init_func = self.config.get('init_func')
        self.job = self.config.get('job')
        self.full_path = os.path.join(self.dirname, self.filename)
        self.source = self.config.get('source')
        self.destination = self.config.get('destination')

        try:
            # setup logging
            self.logger = self._create_logger()
            self.logger.info("START AT {}".format(arrow.now()))
            
            # get new job instance
            if self.job:
                self.job = self._get_job()
                self.job.start()
                self.last_run_date = self.job.most_recent()

                # append last run date to args
                # any compatible script must support a --last_run_date argument
                if self.last_run_date:
                    self.args.append('--last_run_date')
                    self.args.append(str(self.last_run_date)) # **command lien args must be strings**

            # manage path and moduel imports
            self._set_path()
            self._clear_module_cache(module_list=['config', 'config.secrets'])

            # get script module and main function
            self.module = self._script_as_module()
            self.main = getattr(self.module, self.init_func)

            # run the script
            self.results = self.main(self.args)

            # coerce records processed if number retruned from function
            if self.job:
                try:
                    self.records_processed = int(self.results)

                except ValueError:
                    self.records_processed = None

                self.job.result('success', records_processed=self.records_processed)
            return

        except Exception as e:
            self._handle_exception(e)

    
    def _get_config(self):

        with open(self.config_path) as fin:
            scripts_config = yaml.load(fin)

            config = scripts_config.get(self.name)
        
            if config:
                return config
            else:
                raise AttributeError(f"Config not found for script {self.name}")


    def _create_logger(self):
        """
        Args:
            script_name (str): script name
        
        Returns: logger
            a logger class that logs exceptions, start time and end time in the log folder. 
        
        """
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        logfile = f"{self.log_path}/{self.name}.log"

        return logutil.timed_rotating_log(logfile)


    def _get_job(self):
        """Create a named script job to post on job server. Critical for incremental loading.
        
        Args:
            script_name (str): script_name

        Returns:
            job class: 

        """
        return jobutil.Job(
            name=self.name,
            url=secrets.JOB_DB_API_URL,
            source=self.source,
            destination=self.destination,
            auth=secrets.JOB_DB_API_TOKEN,
        )

    def _clear_module_cache(self, module_list=[]):
        # Remove specified moduel from module cache
        # to avoid conflict between imported script modules of same name.
        # I challenge you to find a better way to do this in python 3.5+
        for module_name in module_list:
            sys.modules.pop(module_name)


    def _set_path(self):
        # replace the first entry in the sys path 
        # to match the path of the script to be launched
        # ensures imports work on imported script
        sys.path[0] = self.dirname
        return sys.path


    def _script_as_module(self):
        # import script as module
        # (see: https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path) 
        spec = importlib.util.spec_from_file_location(self.init_func, self.full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


    def _handle_exception(self, e):
        self.logger.error(traceback.format_exc())

        if self.job:
            self.job.result('error', message=str(e))

        raise e


def cli_args():
    """Get command line arguments.
    
    Returns: args_dict
        a dictionary contains all arguments from command line imputs.

    """
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "name",
        help="The unique name of the script to run, as defined in the scripts.yml config."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = cli_args()

    script = Script(
        args.name
    )

    sys.exit()










