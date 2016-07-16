import sys,site
site.addsitedir(sys.path[0]+'\\..\\MyWebsite')  
print (sys.path)  # just verify it is there  

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from MyWebsite.mod_auth.models import User
from MyWebsite.mod_rescue.models import RescueAlert
from datetime import datetime, timedelta
from threading import Thread, Lock, Event
from time import sleep
from alert_process_thread import AlertProcessThread

def get_time_plus_minutes(min):
    now = datetime.now()
    print("Now               = {}".format(now))
    now_plus_min = now + timedelta(minutes=min)
    print("One hour from now = {}".format(now_plus_min))
    return now_plus_min

class AlertProcessEngine():
    def __init__(self):
        self.alert_procs_threads = []

        # Record extractor thread
        self.alert_extractor_thread = None

        # In memory buffer that stores alerts to process.
        # Processing threads requests alerts from this buffer
        self.alerts_buff = []

        self.stop_engine = False
        
        # Lock and Event
        self.alert_list_lock = Lock()
        self.alert_pull_event = Event()
        self.alert_pull_event.clear()

        self.db_engine = create_engine('postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp')

    '''
    num_records = how many records each thread processes at a time
    expirty_time = filter records by their expiry time. 
                   pull records that are expiring between now and (now + expiry_time)
    '''
    def configure_engine(self, expiry_time, num_records, num_thread):
        self.alert_expiry_time = expiry_time
        self.num_alert_process = num_records
        self.num_process_threads = num_thread

    def trigger_extractor(self):
        self.alert_pull_event.set()

    def alert_extractor_worker(self):
        print("Record extractor runner started")
        while(not self.stop_engine):
            if not self.alert_pull_event.is_set():
                print("waiting to pull more events")

            self.alert_pull_event.wait()

            if self.stop_engine:
                print("Engine stopped after waking up")
                break

            self.pull_alerts_from_db()
            self.alert_pull_event.clear()

    def start_record_extractor(self):
        self.alert_extractor_thread = Thread(target=self.alert_extractor_worker,
                                              name="AlertExtractorThread")
        self.alert_extractor_thread.start()

    def start_processing_threads(self):
        for i in range(self.num_process_threads):
            thread_name = "AlertProcessThread" + str(i)
            processor = AlertProcessThread(self)
            processor_thread = Thread(name=thread_name, target= processor.record_process_runner)
            self.alert_procs_threads.append((processor, processor_thread))
            processor_thread.start()

    def start_engine(self):
        # TODO: FIXME: Ensure that engine is configured before starting engine
        self.SessionM = sessionmaker(bind=self.engine)
        self.session = self.SessionM()

        self.start_record_extractor()
        self.start_processing_threads()

    def fetch_alerts_from_mem(self):
        self.alert_list_lock.acquire()
        try:
            ret_list = []
            for i in range(self.num_alert_process):
                ret_list.append(self.alerts_buff[i])

            # remote the first *num* alerts from alert_buff
            del self.alerts_buff[:self.num_alert_process]

            return ret_list
        finally:
            # TODO: FIXME: is this called after return. 
            self.alert_list_lock.release()

    def extract_alerts_from_db(self):
        print("Extracting records from db")
        self.alert_list_lock.acquire()
        try:
            expiry_time = get_time_plus_minutes(self.alert_expiry_time)

            # Pull records from db which are sorted in ascending order
            alerts = self.session.query(RescueAlert).filter(RescueAlert.adventure_end_time > datetime.now(), RescueAlert.adventure_end_time < expiry_time).order_by(asc(RescueAlert.adventure_end_time)).all()

            self.alerts_buff[len(self.alerts_buff): len(self.alerts_buff)] = alerts
            for al in self.alerts_buff:
                print("\t Adventure Name is {}, end-time {}".format(al.adventure_name, al.adventure_end_time))
        finally:
            self.alert_list_lock.release()

    def shutdown_engine(self):
        self.stop_engine = True
        for thread in self.alert_procs_threads:
            thread[0].shutdown()

    def join_worker_threads(self):
        self.alert_extractor_thread.join()
        for thread in self.alert_procs_threads:
            thread[1].join()
