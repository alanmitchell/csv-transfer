#!/usr/bin/python2.7
"""Script to monitor and read CSV files and post records to BMON.

Usage:

    csv_transfer.py CONFIG_FILE

where CONFIG_FILE is the full path name of the script's configuration file,
See README.md for more details.
"""

import glob
import logging
import logging.handlers
import os
import pickle

import sys
import time
import yaml

import readers.csv_reader

# The full directory path to this script file
APP_PATH = os.path.realpath(os.path.dirname(__file__))

# ----- Setup Exception/Debug Logging for the Application

# Log file for the application.
LOG_FILE = os.path.join(APP_PATH, 'log', 'csv_transfer.log')

# Use the root logger for the application.

# stop propagation of messages from the 'requests' module
logging.getLogger('requests').propagate = False

# create a rotating file handler
fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=200000, backupCount=5)

# create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
fh.setFormatter(formatter)

# create a handler that will print to console as well.
console_h = logging.StreamHandler()
console_h.setFormatter(formatter)

# add the handlers to the logger
logging.root.addHandler(fh)
logging.root.addHandler(console_h)

# -------------------

try:
    # configuration file name, 1st command line argument
    config_fn = sys.argv[1]

    # load configuration file describing general operation of this script
    # and the files to be loaded.
    config = yaml.load(open(config_fn))

except:
    logging.exception('Error in Reading Configuration File.')
    sys.exit()

try:
    # set the log level. Because we are setting this on the logger, it will apply
    # to all handlers (unless maybe you set a specific level on a handler?).
    # defaults to INFO if a bad entry in the config file.
    logging.root.setLevel(getattr(logging, config['logging_level'].upper(), 20))

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

    consumers = []
    for consumer in config['consumers']:

        try:
            # Dynamically import the module containing the consumer class

            # pull the class name out of the dictionary.  What remains are the
            # initialization parameters
            class_name = consumer.pop('class_name')

            # all of these modules are located in the 'consumers' folder
            parts = ('consumers.' + class_name).split('.')
            mod = __import__('.'.join(parts[:-1]), fromlist=[parts[-1]])

            # get the consumer class, instantiate it and add it to the
            # consumer list.
            klass = getattr(mod, parts[-1])
            consumers.append(klass(**consumer))

        except:
            logging.exception('Error starting the Consumer %s' % consumer)

except:
    logging.exception('Error in Script Initialization.')
    sys.exit()

# This dictionary maps 'file_type' to a class that is used to read the file.
reader_type_to_class = {'generic': readers.csv_reader.CSVReader}

while True:

    try:
        # Loop through each file spec
        for spec in config['csv_files']:

            try:
                file_pattern = spec.pop('file_glob')
                file_type = spec.pop('file_type', 'generic')
                reader_class = reader_type_to_class[file_type]
                for fn in glob.glob(file_pattern):

                    try:
                        # Files and records must be newer than this timestamp
                        min_ts = last_ts_map.get(fn, 0)

                        # get the Unix timestamp indicating when file was last modified,
                        # and don't process if this file was modified prior to last record
                        # stored.
                        mod_time = os.stat(fn).st_mtime
                        if mod_time <= min_ts:
                            continue

                        recs_processed = 0
                        for recs, last_ts in reader_class(fn, **spec):
                            if last_ts <= min_ts:
                                continue
                            else:
                                # filter down to just records past min_ts
                                recs_filtered = [rec for rec in recs if rec['ts'] > min_ts]
                                recs_processed += len(recs_filtered)
                                for consumer in consumers:
                                    consumer(recs_filtered)
                                last_ts_map[fn] = last_ts
                        if recs_processed:
                            logging.info('%s records processed for file %s' % (recs_processed, fn))

                    except:
                        logging.exception('Error processing file: %s' % fn)

            except:
                logging.exception('Error processing file spec %s' % spec)

        # update the file holding the last processed timestamps by file
        pickle.dump(last_ts_map, open(last_ts_fn, 'wb'))

        if config.get('run_once', False):
            print "Waiting before exit..."
            time.sleep(config.get('run_once_wait_before_stop', 15))
            sys.exit(0)

        # wait before checking again
        time.sleep(config.get('check_interval', 30))

    except SystemExit as e:
        # catch a system exit and exit after proper cleanup
        os._exit(e.code)

    except:
        logging.exception('Error Looping through CSV File Specs.')
        time.sleep(5)
