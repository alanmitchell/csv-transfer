'''Contains the BMONposter class that posts records to a BMON web
application.  See: https://github.com/alanmitchell/bmon
'''
import os
import httpPoster2

# The directory path to this file
THIS_FOLDER = os.path.dirname(__file__)


class BMONposter:
    '''Class to accept a list of timestamped records and post them to a BMON
    web site.  

    Parameters
    ----------
    poster_id:  A unique ID for this BMON poster object, which is used to create file
        names for storing records and recording the last time a record was
        successfully posted.
    bmon_store_url:  The full BMON URL endpoint to post the reords to, for example
        https://bmon.analysisnorth.com/readingdb/reading/store/
    bmon_store_key:  The BMON store key, used for authentication with this particular
        BMON site.
    '''

    def __init__(self, poster_id, bmon_store_url, bmon_store_key):

        # create the HTTP poster to post to BMON
        self.poster = httpPoster2.HttpPoster(post_URL=bmon_store_url,
                                             post_thread_count=1,    # Counter readings must come in order
                                             post_q_filename=os.path.join(THIS_FOLDER, '%s.db' % poster_id),
                                             post_time_file=os.path.join(THIS_FOLDER, '%s.last_post' % poster_id),
                                             )
        self.bmon_store_key = bmon_store_key

    def __call__(self, recs):
        '''Method called to post records. 'recs' is a list of dictionaries, each
        dictionary being one record.  A record has a 'ts' field with a Unix timestamp
        and a variable number of other floating-point fields containing sensor or
        measured data.
        '''

        # create a separate post record for each field in each record
        readings = []
        for rec in recs:
            ts = int(rec.pop('ts'))
            for nm, val in rec.items():
                readings.append((ts, nm, val))

        # add the readings to the Poster object, including the store key
        self.poster.add_readings({'storeKey': self.bmon_store_key, 'readings': readings})
