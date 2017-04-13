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

