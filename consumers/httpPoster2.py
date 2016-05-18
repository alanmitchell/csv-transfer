"""Software to receive sensor readings from data sources and post
them to a HTTP URL.  Readings are cached if an Internet connection 
is not available, or the the post fails for any reason.

Copyright (c) 2014, Alaska Housing Finance Corporation. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this software except in compliance with the License, as included below.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

                             Apache License
                       Version 2.0, January 2004
                    http://www.apache.org/licenses/
TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

Definitions.

"License" shall mean the terms and conditions for use, reproduction, and distribution as defined by Sections 1 through 9 of this document.

"Licensor" shall mean the copyright owner or entity authorized by the copyright owner that is granting the License.

"Legal Entity" shall mean the union of the acting entity and all other entities that control, are controlled by, or are under common control with that entity. For the purposes of this definition, "control" means (i) the power, direct or indirect, to cause the direction or management of such entity, whether by contract or otherwise, or (ii) ownership of fifty percent (50%) or more of the outstanding shares, or (iii) beneficial ownership of such entity.

"You" (or "Your") shall mean an individual or Legal Entity exercising permissions granted by this License.

"Source" form shall mean the preferred form for making modifications, including but not limited to software source code, documentation source, and configuration files.

"Object" form shall mean any form resulting from mechanical transformation or translation of a Source form, including but not limited to compiled object code, generated documentation, and conversions to other media types.

"Work" shall mean the work of authorship, whether in Source or Object form, made available under the License, as indicated by a copyright notice that is included in or attached to the work (an example is provided in the Appendix below).

"Derivative Works" shall mean any work, whether in Source or Object form, that is based on (or derived from) the Work and for which the editorial revisions, annotations, elaborations, or other modifications represent, as a whole, an original work of authorship. For the purposes of this License, Derivative Works shall not include works that remain separable from, or merely link (or bind by name) to the interfaces of, the Work and Derivative Works thereof.

"Contribution" shall mean any work of authorship, including the original version of the Work and any modifications or additions to that Work or Derivative Works thereof, that is intentionally submitted to Licensor for inclusion in the Work by the copyright owner or by an individual or Legal Entity authorized to submit on behalf of the copyright owner. For the purposes of this definition, "submitted" means any form of electronic, verbal, or written communication sent to the Licensor or its representatives, including but not limited to communication on electronic mailing lists, source code control systems, and issue tracking systems that are managed by, or on behalf of, the Licensor for the purpose of discussing and improving the Work, but excluding communication that is conspicuously marked or otherwise designated in writing by the copyright owner as "Not a Contribution."

"Contributor" shall mean Licensor and any individual or Legal Entity on behalf of whom a Contribution has been received by Licensor and subsequently incorporated within the Work.

Grant of Copyright License. Subject to the terms and conditions of this License, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare Derivative Works of, publicly display, publicly perform, sublicense, and distribute the Work and such Derivative Works in Source or Object form.

Grant of Patent License. Subject to the terms and conditions of this License, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except as stated in this section) patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer the Work, where such license applies only to those patent claims licensable by such Contributor that are necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Work to which such Contribution(s) was submitted. If You institute patent litigation against any entity (including a cross-claim or counterclaim in a lawsuit) alleging that the Work or a Contribution incorporated within the Work constitutes direct or contributory patent infringement, then any patent licenses granted to You under this License for that Work shall terminate as of the date such litigation is filed.

Redistribution. You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications, and in Source or Object form, provided that You meet the following conditions:

(a) You must give any other recipients of the Work or Derivative Works a copy of this License; and

(b) You must cause any modified files to carry prominent notices stating that You changed the files; and

(c) You must retain, in the Source form of any Derivative Works that You distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work, excluding those notices that do not pertain to any part of the Derivative Works; and

(d) If the Work includes a "NOTICE" text file as part of its distribution, then any Derivative Works that You distribute must include a readable copy of the attribution notices contained within such NOTICE file, excluding those notices that do not pertain to any part of the Derivative Works, in at least one of the following places: within a NOTICE text file distributed as part of the Derivative Works; within the Source form or documentation, if provided along with the Derivative Works; or, within a display generated by the Derivative Works, if and wherever such third-party notices normally appear. The contents of the NOTICE file are for informational purposes only and do not modify the License. You may add Your own attribution notices within Derivative Works that You distribute, alongside or as an addendum to the NOTICE text from the Work, provided that such additional attribution notices cannot be construed as modifying the License.

You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Works as a whole, provided Your use, reproduction, and distribution of the Work otherwise complies with the conditions stated in this License.

Submission of Contributions. Unless You explicitly state otherwise, any Contribution intentionally submitted for inclusion in the Work by You to the Licensor shall be under the terms and conditions of this License, without any additional terms or conditions. Notwithstanding the above, nothing herein shall supersede or modify the terms of any separate license agreement you may have executed with Licensor regarding such Contributions.

Trademarks. This License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work and reproducing the content of the NOTICE file.

Disclaimer of Warranty. Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.

Limitation of Liability. In no event and under no legal theory, whether in tort (including negligence), contract, or otherwise, unless required by applicable law (such as deliberate and grossly negligent acts) or agreed to in writing, shall any Contributor be liable to You for damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of this License or out of the use or inability to use the Work (including but not limited to damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all other commercial damages or losses), even if such Contributor has been advised of the possibility of such damages.

Accepting Warranty or Additional Liability. While redistributing the Work or Derivative Works thereof, You may choose to offer, and charge a fee for, acceptance of support, warranty, indemnity, or other liability obligations and/or rights consistent with this License. However, in accepting such obligations, You may act only on Your own behalf and on Your sole responsibility, not on behalf of any other Contributor, and only if You agree to indemnify, defend, and hold each Contributor harmless for any liability incurred by, or claims asserted against, such Contributor by reason of your accepting any such warranty or additional liability.

END OF TERMS AND CONDITIONS

APPENDIX: How to apply the Apache License to your work.

To apply the Apache License to your work, attach the following boilerplate notice, with the fields enclosed by brackets "{}" replaced with your own identifying information. (Don't include the brackets!) The text should be enclosed in the appropriate comment syntax for the file format. We also recommend that a file or class name and description of purpose be included on the same "printed page" as the copyright notice for easier identification within third-party archives.

Copyright {yyyy} {name of copyright owner}

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

TO DO:
    * Test separate threads writing to post_time_file simultaneously
    * Perhaps abandon post if it isn't successful after a few retries. It would
        be left in the 'processing' queue, so would get tried again upon a
        restart. This protects against some bad format locking up a post worker.
        But if post is abandoned and Internet comes back, it will be left in
        processing queue.
"""

import time, sys
import threading, json, logging
import requests
import sqlite_queue

# Disable warning messages that result from having to use Python 2.7.3 instead of
# 2.7.9 and from having to disable SSL verification due to problems with Python 2.7.3
# in conjunction with urllib3.
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

class HttpPoster:
    """A class to post readings to a URL via HTTP.  The readings to be posted
    are delivered to this object via the addReadings() method.
    """
    
    def __init__(self, post_URL, 
                       reading_converter=None, 
                       post_q_filename='postQ.sqlite', 
                       post_thread_count=2, 
                       post_time_file='/var/tmp/last_post_time'):
        """Parameters are:
        'post_URL': URL to post the data to.
        'reading_converter': function or callable to convert the format
            of the readings delivered to the "addReadings" method, if
            required.
        'post_q_filename': name of the file to use for implementing the
            queue.
        'post_thread_count': number of post worker threads to start up.
        'post_time_file': name of the file to store the last time that
            a successful post occurred. (Unix timestamp).
        """
        
        self.reading_converter = reading_converter

        # create the queue used to store the readings.
        self.post_Q = sqlite_queue.SqliteReliableQueue(post_q_filename)
        
        # start the posting worker threads
        for i in range(post_thread_count):
            PostWorker(self.post_Q, post_URL, post_time_file).start()
            
    def add_readings(self, reading_data):
        """Adds a set of readings to the posting queue.  The 'reading_data' 
        variable will be converted to JSON and posted to the HTTP server.  So, 
        the server must understand that format.  If there is a converting
        function present, use it to convert the readings.
        """
        if self.reading_converter:
            self.post_Q.append(self.reading_converter(reading_data))
        else:
            self.post_Q.append(reading_data)


class PostWorker(threading.Thread):
    """
    A class to post readings to an HTTP server.
    Make sure the HTTP server responds with a status code of 200 if it receives
    the readings, even though those readings may be badly formatted or duplicates.
    Otherwise, this object will continue to try to repost the bad readings.
    """

    def __init__ (self, source_Q, post_URL, post_time_file):
        """ Create the posting worker in its own thread.
        'sourceQ': the ReadingQueue to get postings from.
        'postURL': the URL to post to, w/o any parameters
        'post_time_file': the name of a file to record the time of 
             a successful post.
        """  
        # run constructor of base class
        threading.Thread.__init__(self)
        
        # If only thing left running are daemon threads, Python will exit.
        self.daemon = True   
        self.source_Q = source_Q
        self.post_URL = post_URL
        self.post_time_file = post_time_file
       
        
    def run(self):
        
        while True:

            try:
                # get the next list of readings to post.  the 'q_id' identifies
                # this set of readings so it can be dropped from queue when 
                # finished.
                q_id, readings = self.source_Q.popleft()
                
                # encode these as json to put into the post
                post_data = json.dumps(readings)
            except:
                logging.exception('Error popping or JSON Encoding readings to post.')
                time.sleep(5)   # to limit rapid fire errors
                continue   # go back and pop another

            retry_delay = 15  # start with a 15 second delay before retrying a post
            while True:
                try:
                    # need to *not* verify SSL requests as Python 2.7.3 has an issue with
                    # requests SSL verification causing to fail when cert is actually OK.
                    req = requests.post(self.post_URL, data=post_data, timeout=15, verify=False)
                    if req.status_code == 200:
                        if logging.root.level == logging.DEBUG:
                            logging.debug('posted: %s, %s' % (readings, req.text))
                        else:
                            logging.info('posted %d bytes' % len(post_data))
                        
                        # tell the queue that this item is complete
                        self.source_Q.finished(q_id)
                        
                        # record the time of the post in the file ignoring
                        # errors (which might be caused by another worker writing
                        # to the file simultaneously.
                        try:
                            fout = open(self.post_time_file, 'w')
                            fout.write(str(time.time()))
                            fout.close()
                        except:
                            pass
                            
                        break   # and get another item from the queue
                        
                    else:
                        raise Exception('Bad Post Status Code: %s' % req.status_code)
                        
                except:
                    logging.exception("Error posting: %s" % readings)
                    time.sleep(retry_delay)   # try again later
                    if retry_delay < 8 * 60:
                        retry_delay *= 2

class BMSreadConverter:
    """Used to create the needed data structure for posting to the BMS application
    server.  Adds the 'storeKey' to a set of readings.
    """

    def __init__(self, store_key):
        self.store_key = store_key

    def __call__(self, readings):
        return {'storeKey': self.store_key, 'readings': readings}

