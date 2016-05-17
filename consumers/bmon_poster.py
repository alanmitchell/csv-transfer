

class BMONposter:

    def __init__(self, bmon_url, bmon_store_key):
        print bmon_url, bmon_store_key

    def __call__(self, recs):
        for rec in recs:
            print rec['ts']
