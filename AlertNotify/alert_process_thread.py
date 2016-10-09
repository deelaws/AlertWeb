'''
AlertWeb module is in a different directory.
Add it to your system path to access it.
'''
import sys,site
site.addsitedir(sys.path[0]+'\\..\\AlertWeb')  
print (sys.path)  # just verify it is there  

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from AlertWeb.mod_auth.models import User
from AlertWeb.mod_rescue.models import RescueAlert
from datetime import datetime, timedelta
from threading import Thread, Lock, Event, current_thread
from time import sleep

class AlertProcessThread():
    def __init__(self, engine,**kwargs):
        self.processing_engine = engine
        self._stop_processing = False
        self._records = []
        return super().__init__(**kwargs)

    '''
    Alert processor method that works on the pulled records.
    '''
    def record_process_runner(self):
        print("*** records process runner thread STARTED ***")
        while(not self._stop_processing):
            print("THREAD {} getting records from Enginge".format(current_thread().name))
            self._records = self.processing_engine.fetch_alerts_from_mem()
            if None == self._records:
                # If no records in the buffer then tell the Enginer Extractor to pull
                # records from memory
                self.processing_engine.trigger_extractor()
            else:
                print("*** processor has {} records to process ***".format(len(self._records)))
                # Pull a couple records from the record buffer.
                # What if the record buffer is empty
                # recods are already sorted.
                for alert in self._records:
                    time_delta =  alert.adventure_end_time - datetime.now()
                    
                    # wait for (currenttime - first record) amount of time.
                    print("\t sleeping for {} seconds".format(time_delta.seconds))
                    if time_delta.days < 0:
                        # time has expired. Send the alert now.
                        print("\t TIME EXPIRED SENDING ALERT NOW.")
                    else:
                        sleep(time_delta.seconds)
                        # wake up and send a message
                        #print("\t\t Sending email for alert which ended at {}".format(alert.adventure_end_time))
                        alert.send_alert()

    def shutdown(self):
        printf("shutting engine down")
        self._stop_processing = True