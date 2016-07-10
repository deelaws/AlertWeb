from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from MyWebsite.mod_auth.models import User
from MyWebsite.mod_rescue.models import RescueAlert
from datetime import datetime, timedelta
from flask_mail import Mail
from threading import Thread, Lock, Event

def get_time_plus_minutes(min):
    now = datetime.now()
    print("Now = {}".format(now))
    now_plus_min = now + timedelta(minutes=min)
    print("One hour from now = {}".format(now_plus_min))
    return now_plus_min

class RecordProcessorCore():
    def __init__(self, num_threads):
        self.stop_extracting = False
        self.record_list_lock = Lock()
        self.record_pull_event = Event()
        self.records = []

        # set the event so that when the record extractor thread is started,
        # it is signaled to pull the events.
        self.record_pull_event.set()
        self.engine = create_engine('postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp')
        
    
    def commence_engine(self): 
        self.SessionM = sessionmaker(bind=self.engine)
        self.session = self.SessionM()

        # Start processing thread
        self.start_record_extractor_thread()

    def record_extractor_runner(self):
        while(not self.stop_extracting):
            if not self.record_pull_event.is_set():
                print("waiting to pull more events")

            self.record_pull_event.wait()
            print("Pulling events")
            time_plus_twenty = get_time_plus_minutes(20)
            alerts = self.session.query(RescueAlert).filter(RescueAlert.adventure_end_time > datetime.now(), RescueAlert.adventure_end_time < time_plus_twenty ).all()
            self.record_list_lock.acquire()
            try:
                self.records[len(self.records): len(self.records)] = alerts
                for al in self.records:
                    print("\t Adventure Name is {}, end-time {}".format(al.adventure_name, al.adventure_end_time))
            finally:
                self.record_list_lock.release()
            self.record_pull_event.clear()

                
    '''
    Start's a thread that pulls records into a central record buffer.
    All record processing threads pull records from that record buffer.
    '''
    def start_record_extractor_thread(self):
        self.record_extractor_thread = Thread(target=self.record_extractor_runner)
        #self.record_extractor_thread.daemon = True
        self.record_extractor_thread.start()
        

    '''
    Starts the specified number of threads that process records.
    '''
    def start_record_processing_threads(self, num_threads):
        pass

    '''
        pulls records from database
    '''
    def pull_records(self):
        self.record_list_lock.acquire()
        try:
            print("Pulling records from database")
        finally:
            self.record_list_lock.release()


if __name__ == "__main__":
    print("Starting Record Processor Engine")
    rpc =  RecordProcessorCore(1)
    rpc.commence_engine()
    rpc.record_extractor_thread.join()
    while("exit" != input("enter exit to quit\n")):
        print("\t Continuing to process records")

    print("Exiting processing")
    