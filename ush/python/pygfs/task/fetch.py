#!/usr/bin/env python3

import os
from logging import getLogger
from typing import Any, Dict, List

from wxflow import (AttrDict, FileHandler, Hsi, Task,
                    logit, parse_j2yaml)
from wxflow import htar as Htar
import tarfile


logger = getLogger(__name__.split('.')[-1])


class Fetch(Task):
    """Task to pull ROTDIR data from HPSS (or locally)
    """

    @logit(logger, name="Fetch")
    def __init__(self, config: Dict[str, Any]) -> None:
        """Constructor for the Fetch task
        The constructor is responsible for collecting necessary yamls based on
        the runtime options and RUN.

        Parameters
        ----------
        config : Dict[str, Any]
            Incoming configuration for the task from the environment

        Returns
        -------
        None
        """
        super().__init__(config)
        # Perhaps add other stuff to self.

    @logit(logger)
    def configure(self, fetch_dict: Dict[str, Any]):
        """Determine which tarballs will need to be extracted

        Parameters
        ----------
        fetch_dict : Dict[str, Any]
            Task specific keys, e.g. COM directories, etc

        Return
        ------
        parsed_fetch: Dict[str, Any]
           Dictionary derived from the yaml file with necessary HPSS info.
        """
        self.hsi = Hsi()

        fetch_yaml = fetch_dict.fetch_yaml
        fetch_parm = os.path.join(fetch_dict.PARMgfs, "fetch")

        parsed_fetch = parse_j2yaml(os.path.join(fetch_parm, fetch_yaml),
                                    fetch_dict)
        return parsed_fetch

    @logit(logger)
    def execute_pull_data(self, atardir_set: Dict[str, Any]) -> None:
        """Pull data from HPSS based on a yaml dictionary and store at the
           specified destination.

        Parameters
        ----------
        atardir_set: Dict[str, Any],
            Dict defining set of tarballs to pull and where to put them.

        Return
            None
        """

        if len(f_names) <= 0:     # Abort if no files
            raise FileNotFoundError("FATAL ERROR: The tar ball has no files")
        f_names = atardir_set.untar.contents
        on_hpss = atardir_set.untar.on_hpss
        dest = atardir_set.untar.destination
        # Select action whether no_hpss is True or not, and pull these
        #    data from tape or locally and place where it needs to go
        # DG - these need testing
        if on_hpss is True:  # htar all files in fnames
            htar_obj = Htar.Htar()
            htar_obj.cvf(dest, f_names)

        else:  # tar all files in fnames
            with tarfile.open(dest, "w") as tar:
                for filename in f_names:
                    tar.add(filename)
