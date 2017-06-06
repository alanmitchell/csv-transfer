"""Class to read CSV files generated by a Siemens building automation system.

Here is a sample file that can be read:

"Key            Name:Suffix                                Trend Definitions Used"
"Point_1:","CCHRC.BLR2.FUEL","","COV         1 hour"
"Point_2:","CCHRC.DEM:CONSUMPTN HI","","COV         1 minute"
"Point_3:","CCHRC.DEM:CONSUMPTN LO","","COV         1 minute"
"Point_4:","CCHRC.HRV1.CO2","","15 minutes"
"Point_5:","CCHRC.HRV1.RMH","","15 minutes"
"Point_6:","CCHRC.HRV1.RMT","","15 minutes"
"Point_7:","CCHRC.OAT","","15 minutes"
"Time Interval:","5 Minutes"
"Date Range:","6/5/2017 00:00:00 - 6/5/2017 23:59:59"
"Report Timings:","All Hours"
""
"<>Date","Time","Point_1","Point_2","Point_3","Point_4","Point_5","Point_6","Point_7"
"6/5/2017","00:00:00","2480.7764","1062912","No Data","550.76","24.31","70.57","65.5"
"6/5/2017","00:05:00","2480.7764","1062912","No Data","550.76","24.31","70.57","64.8"
"6/5/2017","00:10:00","2480.7764","1062912","No Data","550.76","24.31","70.57","64.8"
"6/5/2017","00:15:00","2480.7764","1062912","No Data","558.64","24.31","70.51","64.5"
"6/5/2017","00:20:00","2480.7764","1062912","No Data","558.64","24.31","70.51","64.5"

"""
import csv
import calendar
import logging
import math
import pytz
from dateutil import parser

# the error logger to use for this module
logger = logging.getLogger(__name__)


class SiemensReader:
    pass