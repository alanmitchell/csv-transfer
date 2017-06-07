"""Function to read CSV files generated by a Siemens building automation system
running Insight management software, version 5.

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
import string
import pytz
from dateutil import parser

# the error logger to use for this module
logger = logging.getLogger(__name__)


def clean_string(s):
    """Function that "cleans" a string by first stripping leading and trailing
    whitespace and then substituting an underscore for all other whitepace
    and punctuation. After that substitution is made, any consecutive occurrences
    of the underscore character are reduced to one occurrence. Returns the cleaned string.

    Input Parameters:
    -----------------
    s:  The string to clean.
    """
    to_sub = string.whitespace + string.punctuation
    trans_table = string.maketrans(to_sub, len(to_sub) * '_')
    fixed = string.translate(s.strip(), trans_table)

    while True:
        new_fixed = fixed.replace('_' * 2, '_')
        if new_fixed == fixed:
            break
        fixed = new_fixed

    return fixed


def siemens_reader(filename, chunk_size=1, ts_tz='UTC', field_names=[], exclude_fields=[],
                 **csv_params):
    """This generator function reads CSV report files from a Siemens
    building automation system running Insight (version 5) software.
    The function yields chunks of records from those files.
    A chunk of records is a list of dictionaries, each dictionary being one record.
    A record has a 'ts' field, which is a UNIX timestamp (seconds from the epoch).
    All other fields that are to be included are converted to a float number; if the
    field value is not a number, that field is deleted from the returned record (but may
    occur in other records, if valid numeric values are present in those records).
    Thus, each record returned has a Unix timestamp and a number of fields, each of which is a
    floating point number.

    Each iteration of this generator returns a two tuple:
        * a list of records, the length of which is determined by 'chunk_size',
        * the Unix timestamp of the last record in that set.

    Example Usage:
        for recs, last_ts in siemens_reader('test.csv', chunk_size=10):
            print recs, last_ts

    Parameters
    ----------
    filename:  Required.  The full path to the CSV file to be read.
    chunk_size: The number of records to return with each iteration.  Default is 1.
        If more than one record is returned, the return value from the iterator is a list
        of records.
    ts_tz:  The timezone from the Olson database of the timestamps found in the CSV file.
        This parameter defaults to "UTC".  An example of another suitable value is
        "America/Anchorage".
    field_names:  This is a list of field names to assign to each Point column in the CSV file.
        If this list is empty (the default), the class uses the Point names that are
        present in the CSV file as the field names.  However, the Point names present
        in the CSV file are translated to substitute underscore (_) characters for all
        spaces and punctuation found in the Point name.  In addition, if that
        substitution results in consecutive underscores, only one underscore is
        retained.
    exclude_fields:  A list of field names to exclude from the final records returned.
        These field names must be written in their final form, i.e. as one of the
        'field_names' items, or as one of the translated Point names if field_names
        are not provided.
    **csv_params:  Any other keyword arguments found are passed along to the csv.Reader
        initialization function and can be used to correctly specify delimiters and
        quoting formats found in the CSV file.
    """

    recs = []
    tstz = pytz.timezone(ts_tz)
    with open(filename) as csvfile:

        reader = csv.reader(csvfile, **csv_params)

        # read all lines through the header row, gathering up
        # point names along the way.
        names = []
        ln = reader.next()
        while ln[0] != '<>Date':
            if ln[0].startswith('Point_'):
                names.append(clean_string(ln[1]))
            ln = reader.next()

        # if field names are specified, use those.
        # Strip white space from names.
        if len(field_names):
            names = [fld.strip() for fld in field_names]

        last_ts = 0
        for row in reader:

            # skip rows with less than 3 fields
            if len(row) < 3:
                continue

            try:

                # make a dictionary from the values, with keys as the field names
                # Values are found in the 3rd column onward.
                rec = dict(zip(names, row[2:]))

                # make the timestamp
                dt_str = ' '.join(row[:2])
                dt = parser.parse(dt_str)
                dt = tstz.localize(dt)
                rec['ts'] = calendar.timegm(dt.utctimetuple())

                # remove fields to exclude
                for fld in exclude_fields:
                    rec.pop(fld, None)

                # remember last timestamp.
                last_ts = rec['ts']

                # convert all fields to floats (redundant for 'ts' field)
                for k, v in rec.items():
                    try:
                        rec[k] = float(v)
                        # do not include NaN values
                        if math.isnan(rec[k]):
                            del rec[k]
                    except:
                        # if value isn't a number, drop this field in this record
                        del rec[k]

                recs.append(rec)

                # if we have accumulated the desired number of records, release them
                if len(recs) == chunk_size:
                    if chunk_size != 1:
                        yield recs, last_ts
                    else:
                        # yield the individual record, not a 1-element list
                        yield recs[0], last_ts
                    recs = []
            except:
                logger.exception('Error processing record from file %s: %s' % (filename, row))

        # there may be a partial chunk to yield.
        if len(recs):
            yield recs, last_ts
