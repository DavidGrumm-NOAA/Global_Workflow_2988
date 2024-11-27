#!/usr/bin/env python3

import os

from fetch import Fetch
from wxflow import AttrDict, Logger, cast_strdict_as_dtypedict, logit

# initialize root logger
logger = Logger(level=os.environ.get("LOGGING_LEVEL", "DEBUG"), colored_log=True)


@logit(logger)
def main():

    config = cast_strdict_as_dtypedict(os.environ)

    # Instantiate the Fetch object
    fetch = Fetch(config)

    # Pull out all the configuration keys needed to run the fetch step
    keys = ['current_cycle', 'RUN', 'PDY', 'PARMgfs', 'PSLOT', 'ROTDIR', 'fetch_yaml', 'ATARDIR', 'ntiles']

    fetch_dict = AttrDict()
    for key in keys:
        fetch_dict[key] = fetch.task_config.get(key)
        if fetch_dict[key] is None:
            print(f"Warning: key ({key}) not found in task_config!")

    # Also import all COMOUT* directory and template variables
    for key in fetch.task_config.keys():
        if key.startswith("COMOUT_"):
            fetch_dict[key] = fetch.task_config.get(key)
            if fetch_dict[key] is None:
                print(f"Warning: key ({key}) not found in task_config!")

    # Determine which archives to retrieve from HPSS
    # Read the input YAML file to get the list of tarballs on tape
    atardir_set = fetch.configure(fetch_dict)

    # Pull the data from tape or locally and store the specified destination
    fetch.execute_pull_data(atardir_set)


if __name__ == '__main__':
    main()
