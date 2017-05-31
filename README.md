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
        chunk_size: 10
        header_rows: 4
        name_row: 2
        field_map: "lambda nm: '_'.join(nm.split('_')[:2])"
        ts_tz: America/Anchorage
        exclude_fields: [RECORD]

The `csv_files` element in the YAML file allows for entering a list of different file specifications; each specification in the list represents a set of CSV files that will be processed and potentially monitored for changes by the script.  The excerpt from the YAML file above shows one file specification, a spec that processes all CSV files ending with `.csv` that are present in the directory where the script was executed; additional file specs could be entered as additional list elements under the `csv_files` element.  The only required element in a file specification is the `file_glob` entry.  This string (enclosed in double quotes) should be compatible with the Python `glob.glob` function and directs the script to process the files returned by the `glob` function.  The other elements in the file specification are first passed to the constructor of the `csv_reader.CSVReader` class; if an element does not match one of the constructor parameters, it is forwarded on to the `csv.reader` function found in the standard `csv` Python module.  This structure allows for substantial control over how the CSV files are read by this script.

Here is an extract from the documentation of the constructor parameters of the `csv_reader.CSVReader` class, which is the first stop for the elements found in the file specification.

    chunk_size: The number of records to return with each iteration.  Default is 1.
        If more than one record is returned, the return value from the iterator is a list
        of records.
    ts_field:  The name of the field that is the timestamp field.  Default value is None,
        which means that the timestamp field is the first field (column) in the CSV file.
        The timestamp field can be expressed as a Unix timestamp in seconds past the epoch, 
        or the field can be a date/time string that is able to be parsed by 
        dateutil.parser.parse.
    ts_tz:  The timezone from the Olson database of the timestamps found in the CSV file.
        If the timestamp in the file is a floating point number, it is assumed to already
        be a Unix timestamp expressed in seconds past the UTC epoch.  For string
        timestamps, this parameter is relevant and defaults to "UTC".  An example of
        another suitable value is "America/Anchorage".
    field_names:  This is a list of field names to assign to each column in the CSV file.
        If this list is empty (the default), the class looks to the Header row in the file 
        to determine field names.
    header_rows:  This is the number of rows at the beginning of the file that do not
        contain records.  The default value is 1.  These header rows may or may not contain
        a field names row.  These rows are read out of the file before processing records.
    name_row:  This gives the row number where the field names are located; the first row
        is row number 1, and the default value is 1.  If the 'field_names' list is
        populated than this 'name_row' value is ignored.
    field_map:  This is a dictionary or a lambda function expressed as a string that is
        used to convert the field names found in a header row.  The dictionary maps
        original names to new names; it need not cover all original names.  Names not
        present in the dictionary are kept the same.  If 'field_map' is a string, then it
        should be a lambda function; it is processed with 'eval', and the resulting
        function is applied to all of the field names found in the header row.
    exclude_fields:  A list of field names to exclude from the final records returned.
    **csv_params:  Any other keyword arguments found are passed along to the csv.Reader
        initialization function and can be used to correctly specify delimiters and
        quoting formats found in the CSV file.

The `csv_files` element, described above, controls which CSV files are read by the script.  After these CSV files are read and parsed, they are passed on to one or more consumers of the time-stamped records.  Currently, there is one consumer available in this project, a class that knows how to take the records and post the data to the [BMON Web-based Sensor Analysis software](https://github.com/alanmitchell/bmon).  Below is the `consumers` portion of the configuration file, which holds a list of one or more record consumers.  The example below has one consumer, which directs the script to send the records to the `bmon_poster` consumer:

    consumers:
      - class_name: bmon_poster.BMONposter
        poster_id:  an-bmon-01              # unique ID for this posting object
        bmon_store_url: https://bmon.analysisnorth.com/readingdb/reading/store/
        bmon_store_key: xyz123

Each consumer must contain a `class_name` element, which specifies the Python class that implements the consumer.  All of the consumers are located in the `consumers` directory of the project.  For the `bmon_poster` consumer, the class is found in the `bmon_poster` module and has the class name `BMONposter`, as indicated by the `class_name` entry above. This particular consumer also needs additional information to operate, and so there are three additional elements in the consumer specification:

`poster_id` is a string that identifies this particular consumer.  It is used to create various files needed for operation of the BMON poster.

The `bmon_store_url` is the full URL to the storage function of the BMON server. Also, each BMON server has a unique and secret storage key string; providing this string is required for storing data on the BMON server.  That should be entered in the `bmon_store_key` element.