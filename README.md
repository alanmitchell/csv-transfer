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

This determines how much information will be recorded to the script's log file.  Possible values are `CRITICAL, ERROR, WARNING, INFO, DEBUG`, with `CRITICAL` recording the least amount of information and `DEBUG` recording the most.  The log file is located in the same directory as the `csv_transfer.py` script and has the name `csv_transfer.log`.

    csv_files:
      - file_glob: "*.csv"
        file_type: generic
        chunk_size: 10
        header_rows: 4
        name_row: 2
        field_map: "lambda nm: '_'.join(nm.split('_')[:2])"
        ts_tz: America/Anchorage
        exclude_fields: [RECORD]

The `csv_files` element in the YAML file allows for entering a list of different file specifications; each specification in the list represents a set of CSV files that will be processed and potentially monitored for changes by the script.  The excerpt from the YAML file above shows one file specification, a spec that processes all CSV files ending with `.csv` that are present in the directory where the script was executed; additional file specs could be entered as additional list elements under the `csv_files` element.  The only required element in a file specification is the `file_glob` entry.  This string (enclosed in double quotes) should be compatible with the Python `glob.glob` function and directs the script to process the files returned by the `glob` function.

The `file_type` element in the specification indicates the specific file reader function to be used to read the CSV file.  This element is not required and defaults to the `generic` file reader, which has the ability, with proper configuration, to read a wide variety of CSV files.  The other possible `file_type` currently available is the `siemens` file type; the associated file reader can read CSV files produced by a Siemens building automation system running the Apogee Insight version 5 software.

Each `file_type` has an associated file reader function found in the `readers` package subdirectory of this project.  The `generic` file type uses the `readers.generic.generic_reader` function to read the CSV files.  The `siemens` file type uses the `readers.siemens.siemens_reader` function to read the CSV files.  Other file types can be added by writing an appropriate file reader function and then adding an element to the file_type-to-function dictionary found in the `csv_transfer.py` file:

    # This dictionary maps 'file_type' to a generator function that is used
    # to read the file.
    file_type_to_func = {'generic': readers.generic.generic_reader,
                         'siemens': readers.siemens.siemens_reader}

The elements in the file specification aside from `file_glob` and `file_type` are first passed to the file reader function associated with the `file_type`.  See the documentation of the parameter list for the reader function to see what elements are possible. In the example specification above, the `chunk_size`, `header_rows`, `name_row`, `field_map`, `ts_tz` and `exclude_fields` elements are passed to the `readers.generic.generic_reader` function.  If an element does not match one of the parameters of the reader function, it is forwarded on to the `csv.reader` function found in the standard `csv` Python module.  This structure allows for substantial control over how the CSV files are read by this script.

The `file_glob` element, described above, controls which CSV files are read by the script.  After these CSV files are read and parsed, they are passed on to one or more consumers of the time-stamped records.  Currently, there is one consumer available in this project, a class that knows how to take the records and post the data to the [BMON Web-based Sensor Analysis software](https://github.com/alanmitchell/bmon).  Below is the `consumers` portion of the configuration file, which holds a list of one or more record consumers.  The example below has one consumer, which directs the script to send the records to the `bmon_poster` consumer:

    consumers:
      - class_name: bmon_poster.BMONposter
        poster_id:  an-bmon-01              # unique ID for this posting object
        bmon_store_url: https://bmon.analysisnorth.com/readingdb/reading/store/
        bmon_store_key: xyz123

Each consumer must contain a `class_name` element, which specifies the Python class that implements the consumer.  All of the consumers are located in the `consumers` directory of the project.  For the `bmon_poster` consumer, the class is found in the `bmon_poster` module and has the class name `BMONposter`, as indicated by the `class_name` entry above. This particular consumer also needs additional information to operate, and so there are three additional elements in the consumer specification:

`poster_id` is a string that identifies this particular consumer.  It is used to create various files needed for operation of the BMON poster.

The `bmon_store_url` is the full URL to the storage function of the BMON server. Also, each BMON server has a unique and secret storage key string; providing this string is required for storing data on the BMON server.  That should be entered in the `bmon_store_key` element.
