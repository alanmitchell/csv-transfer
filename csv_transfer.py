#!/usr/bin/python2.7
"""Script to monitor and read CSV files and post records to BMON.

*** TO DO
- Implement Loging
- Implement a list of "consumers" to use the records.
    - Have a new section in the config file for consumers, each with any custom
      initialization parameters.  Use the __call__ function to process the
      records in the consumer.
"""

import os
import sys
import time
import glob
import logging
import pickle
import yaml
import csv_reader

# change into this directory
os.chdir(os.path.dirname(__file__))

# get a logger for error logging
logger = logging.getLogger('csv_to_bmon')

# configuration file name
config_fn = sys.argv[1]

# load the times of the last record loaded for each file
# The keys of the dictionary are file names and the values
# are the Unix timestamp of the last record loaded.
# This is file is in Python pickle format, and it is named
# the same as the config file, except with a 'last_ts' extension.
last_ts_fn = '%s.last_ts' % config_fn
if os.path.exists(last_ts_fn):
    last_ts_map = pickle.load(open(last_ts_fn, 'rb'))
else:
    last_ts_map = {}

# load configuration file describing general operation of this script
# and the files to be loaded.
config = yaml.load(open(config_fn))

while True:

    # Loop through each file spec
    for spec in config['csv_files']:

        file_pattern = spec.pop('file_glob')
        for fn in glob.glob(file_pattern):

            # Files and records must be newer than this timestamp
            min_ts = last_ts_map.get(fn, 0)

            # get the Unix timestamp indicating when file was last modified,
            # and don't process if this file was modified prior to last record
            # stored.
            mod_time = os.stat(fn).st_mtime
            if mod_time <= min_ts:
                continue

            for recs, last_ts in csv_reader.CSVReader(fn, **spec):
                if last_ts <= min_ts:
                    continue
                else:
                    # filter down to just records past min_ts
                    recs_filtered = [rec for rec in recs if rec['ts'] > min_ts]
                    print recs_filtered
                    last_ts_map[fn] = last_ts

    # update the file holding the last processed timestamps by file
    pickle.dump(last_ts_map, open(last_ts_fn, 'wb'))

    # run only one time during testing
    break

    # wait before checking again
    time.sleep(config['check_interval'])
