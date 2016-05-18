'''Contains the BMONposter class that posts records to a BMON web
application.  See: https://github.com/alanmitchell/bmon
'''
import os
import httpPoster2

# The directory path to this file
THIS_FOLDER = os.path.dirname(__file__)


class BMONposter:

    def __init__(self, poster_id, bmon_store_url, bmon_store_key):

        # create the HTTP poster to post to BMON
        self.poster = httpPoster2.HttpPoster(post_URL=bmon_store_url,
                                             post_q_filename=os.path.join(THIS_FOLDER, '%s.db' % poster_id),
                                             post_time_file=os.path.join(THIS_FOLDER, '%s.last_post' % poster_id),
                                             )
        self.bmon_store_key = bmon_store_key

    def __call__(self, recs):

        # create a separate post record for each field in each record
        readings = []
        for rec in recs:
            ts = int(rec.pop('ts'))
            for nm, val in rec.items():
                readings.append((ts, nm, val))

        # add the readings to the Poster object, including the store key
        self.poster.add_readings({'storeKey': self.bmon_store_key, 'readings': readings})
