"""Class to read CSV files and create timestamped records.
"""
import csv
import calendar
import logging
import math
import pytz
from dateutil import parser

# the error logger to use for this module
logger = logging.getLogger(__name__)


class CSVReader:
    """This class is used to read CSV files and return chunks of records from those files.
    A chunk of records is a list of dictionaries, each dictionary being one record.
    One of the fields (columns) in the file must be a timestamp column, and that field is
    returned as a UNIX timestamp (seconds from the epoch) and has the key value of 'ts'.
    All other fields that are to be included are converted to a float number; if the
    field value is not a number, that field is deleted from the returned record (but may
    occur in other records, if valid numeric values are present in those records).
    Thus, each record returned has a Unix timestamp and a number of fields, each of which is a
    floating point number.

    The object created from this class is iterable, with each iteration returning a two
    tuple:
        * a list of records, the length of which is determined by 'chunk_size',
        * the Unix timestamp of the last record in that set.

    Example Usage:
        for recs, last_ts in CSVReader('test.csv', chunk_size=10):
            print recs, last_ts

    Parameters
    ----------
    filename:  Required.  The full path to the CSV file to be read.
    chunk_size: The number of records to return with each iteration.  Default is 1.
        If more than one record is returned, the return value from the iterator is a list
        of records.
    ts_field:  The name of the field that is the timestamp field.  Default value is None,
        which means that the timestamp field is the first field (column) in the CSV file.
        The timestamp field can be expressed as a Unix timestamp in seconds past the epoch,
        or the field can be a date/time string that is able to be parsed
        by dateutil.parser.parse.
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
        These field names must be written in their final form, i.e. as one of the
        'field_names' items, or after translation by the 'field_map' parameter.
    **csv_params:  Any other keyword arguments found are passed along to the csv.Reader
        initialization function and can be used to correctly specify delimiters and
        quoting formats found in the CSV file.
    """

    def __init__(self, filename, chunk_size=1, ts_field=None, ts_tz='UTC',
                 field_names=[], header_rows=1, name_row=1,
                 field_map={}, exclude_fields=[],
                 **csv_params):

        self.filename = filename
        self.chunk_size = chunk_size
        self.ts_field = ts_field
        self.ts_tz = ts_tz
        self.field_names = field_names
        self.header_rows = header_rows
        self.name_row = name_row
        self.field_map = field_map
        self.exclude_fields = exclude_fields
        self.csv_params = csv_params

    def __iter__(self):

        recs = []
        tstz = pytz.timezone(self.ts_tz)
        with open(self.filename) as csvfile:

            reader = csv.reader(csvfile, **self.csv_params)

            # read the header rows into a list
            headers = [reader.next() for i in range(self.header_rows)]

            # if field names are specified, use those.  If not, use the proper
            # header row and apply the field_map to possibly change names.
            # Strip white space from names.
            if len(self.field_names):
                names = [fld.strip() for fld in self.field_names]
            else:
                names = headers[self.name_row - 1]    # name_row is 1-based
                names = [fld.strip() for fld in names]
                if isinstance(self.field_map, dict):
                    # field map is a dictionary, mapping some/all old names to
                    # new names
                    names = [self.field_map.get(fld, fld) for fld in names]
                elif isinstance(self.field_map, str):
                    # field map is a string, presumed to be a lambda function for
                    # converting field names
                    try:
                        conv_func = eval(self.field_map)
                        names = [conv_func(nm) for nm in names]
                    except:
                        raise ValueError('The field_map function "%s" is not valid.' % self.field_map)

            # Change the timestamp field name to 'ts'
            if not self.ts_field:
                # if no timestamp field is given, use the first column for the timestamp
                names[0] = 'ts'
            else:
                # find the requested field and set its name to 'ts'
                try:
                    names[names.index(self.ts_field)] = 'ts'
                except ValueError:
                    raise ValueError('The requested timestamp field, %s, is not present.' % self.ts_field)

            last_ts = 0
            for row in reader:

                # skip blank rows
                if not len(row):
                    continue

                try:
                    # make a dictionary from the values, with keys as the field names
                    rec = dict(zip(names, row))

                    # remove fields to exclude
                    for fld in self.exclude_fields:
                        rec.pop(fld, None)

                    # make timestamp a Unix epoch timestamp
                    try:
                        # assume field is already Unix epoch timestamp
                        rec['ts'] = float(rec['ts'])
                    except:
                        # treat this as a string date
                        dt = parser.parse(rec['ts'])
                        dt = tstz.localize(dt)
                        rec['ts'] = calendar.timegm(dt.utctimetuple())

                    if math.isnan(rec['ts']):
                        raise ValueError('Timestamp cannot be NaN.')

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
                    if len(recs) == self.chunk_size:
                        if self.chunk_size != 1:
                            yield recs, last_ts
                        else:
                            # yield the individual record, not a 1-element list
                            yield recs[0], last_ts
                        recs = []
                except:
                    logger.exception('Error processing record from file %s: %s' % (self.filename, row))

            # there may be a partial chunk to yield.
            if len(recs):
                yield recs, last_ts
