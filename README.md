# csv-transfer

### A Utility for Reading and Processing time-stamped Records from CSV files

##### Copyright (c) 2016, Analysis North.  All Rights Reserved.

This script reads CSV files that hold time-stamped records of sensor or other numeric values and then transfers those records to web services or other consumers of such records.  The script has the ability to monitor a directory for the addition or update of CSV files, and the script will automatically process those new files.

The script allows for pluggable consumers of the time-stamped records.  Initially, there is one such consumer available: a consumer that posts records to the [BMON Web-Based Sensor Analysis System](https://github.com/alanmitchell/bmon).

Usage of the script is:

    csv-transfer.py CONFIG_FILE

where the `CONFIG_FILE` is a full path to the script's configuration file.  This file determines which CSV files are processed by the script and determines which consumers receive records from the CSV files.  Documentation of the configuration file follows in the next section.

### Configuration File

The configuration file controls the operation of the script.  The file is in [YAML](http://yaml.org/) format.  A number of tutorials are available on the web for learning YAML syntax, including [this one](https://learn.getgrav.org/advanced/yaml).  The rest of the section will walk through the various settings that appear in the configuration file.There is a sample configuration file available [here](sample_config.yaml).

Configuration settings will be presented as a sample setting followed by discussion of the setting.

    run_once: True

If you want the script to run only once and not to continually scan for new or updated CSV files, set the `run_once` setting to `True`.

    run_once_wait_before_stop: 15

If you have set `run_once` to `True`, you many need to cause a delay to occur before exiting the script in order for the consumer of the records to have time to finish processing the records.  This is necessary if one or more of your record consumers operate in a thread separate from the main thread.  The `BMONposter` consumer does operate in a separate thread, so set `run_once_wait_before_stop` to enough seconds of delay to allows for posting of the records.

    check_interval: 30

If `run_once` is set to `False`, the script will scan continually to look for updated or new CSV files.  This `check_interval` setting determines how often the rescan occurs.  It is expressed in seconds.

    logging_level: INFO

This determines how much information will be recorded to the script's log file.  Possible values are `CRITICAL, ERROR, WARNING, INFO, DEBUG`, with `CRITICAL` recording the least amount of information and `DEBUG` recording the most.  On the Raspberry Pi, the log file is located in the same directory as the `csv_transfer.py` script and has the name `csv_transfer.log`.

    csv_files:
      - file_glob: "*.csv"            
        chunk_size: 10
        header_rows: 4
        name_row: 2
        field_map: "lambda nm: '_'.join(nm.split('_')[:2])"
        ts_tz: America/Anchorage
        exclude_fields: [RECORD]

The `csv_files` element in the YAML file allows for entering a list of different file specifications; each specification in the list represents a set of CSV files that will be processed and potentially monitored for changes by the script.  The excerpt from the YAML file above shows one file specification, a spec that processes all CSV files ending with `.csv` that are present in the directory where the script was executed; additional file specs could be entered as additional list elements under the `csv_files` element.  The only required element in a file specification is the `file_glob` entry.  This string (enclosed in double quotes) should be compatible with the Python `glob.glob` function and directs the script to process the files returned by the `glob` function.  The other elements in the file specification are first passed to the constructor of the csv_reader.CSVReader class; if an element does not match on the constructor parameters, it is forwarded on to the `csv.reader` function found in the standard `csv` Python module.  This structure allows for substantial control over how the CSV files are read by this script.

