# csv-transfer
This script reads CSV files that hold time-stamped records of sensor or other numeric values and then
posts or exports those records to web services or other consumers of such records.  The script allows
for pluggable consumers of time-stamped records.  Initially, there is one such consumer coded: a 
consumer that posts records to the [BMON Web-Based Sensor Analysis System](https://github.com/alanmitchell/bmon).
