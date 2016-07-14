from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from MyWebsite.mod_auth.models import User
from MyWebsite.mod_rescue.models import RescueAlert
from datetime import datetime, timedelta
from flask_mail import Mail
from threading import Thread, Lock, Event
from time import sleep

def get_time_plus_minutes(min):
    now = datetime.now()
    print("Now               = {}".format(now))
    now_plus_min = now + timedelta(minutes=min)
    print("One hour from now = {}".format(now_plus_min))
    return now_plus_min

class RecordProcessorCore():
    def __init__(self, num_threads):
        self.stop_extracting = False
        self.record_list_lock = Lock()
        self.record_pull_event = Event()
        self.record_pull_event.clear()
        self.records = []
        self.num_threads = num_threads
        self.processor_threads = []

        # set the event so that when the record extractor thread is started,
        # it is signaled to pull the events.
        self.record_pull_event.set()
        self.engine = create_engine('postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp')

    def shutdown(self):
        self.stop_extracting = True

    def commence_engine(self): 
        self.SessionM = sessionmaker(bind=self.engine)
        self.session = self.SessionM()

        # Start Extractor thread
        self.start_record_extractor_thread()

        # Start Processing Threads
        self.start_record_processing_threads(self.num_threads)

    def record_extractor_runner(self):
        print("record extractor runner started")
        while(not self.stop_extracting):
            if not self.record_pull_event.is_set():
                print("waiting to pull more events")

            self.record_pull_event.wait()

            if self.stop_extracting:
                print("gahhhhh")
                break

            self.pull_records_from_db()
            self.record_pull_event.clear()

    '''
    Record processor method that works on the pulled records.
    '''
    def record_process_runner(self):
        print("*** records process runner thread STARTED ***")
        while(not self.stop_extracting):
            records = self.pull_records_from_mem(3)
            if None == records:
                # If no records in the buffer then tell the extractor to pull
                # records from memory
                self.record_pull_event.set()
            else:
                print("*** processor has {} records to process ***".format(len(records)))
                # Pull a couple records from the record buffer.
                # What if the record buffer is empty
                # recods are already sorted.
                for alert in records:
                    time_delta =  alert.adventure_end_time - datetime.now()
                    
                    # wait for (currenttime - first record) amount of time.
                    print("\t sleeping for {} seconds".format(time_delta.seconds))
                    if time_delta.days < 0:
                        # time has expired. Send the alert now.
                        print("\t TIME EXPIRED SENDING ALERT NOW.")
                    else:
                        sleep(time_delta.seconds)
                        # wake up and send a message
                        print("\t\t Sending email for alert which ended at {}".format(alert.adventure_end_time))

    '''
    Start's a thread that pulls records into a central record buffer.
    All record processing threads pull records from that record buffer.
    '''
    def start_record_extractor_thread(self):
        self.record_extractor_thread = Thread(target=self.record_extractor_runner)
        self.record_extractor_thread.start()

    '''
    Starts the specified number of threads that process records.
    '''
    def start_record_processing_threads(self, num_threads):
        for i in range(self.num_threads):
            th = Thread(target=self.record_process_runner)
            th.start()
            self.processor_threads.append(th)
    
    '''
    Pulls specified number(num) records from records buffer.
    '''
    def pull_records_from_mem(self, num):
        self.record_list_lock.acquire()
        try:
            if len(self.records) < num:
                return None
            else:
                ret_list = []
                for i in range(num):
                    ret_list.append(self.records[i])

                # remove the first *num* elements from record buffer
                del self.records[:num]
                
                return ret_list
        finally:
            self.record_list_lock.release()

    '''
    Pulls records from database
    '''
    def pull_records_from_db(self):
        print("pull records form db")
        self.record_list_lock.acquire()
        try:
            print("Pulling records from database")
            
            # pull records that will expire in 20 minutes
            # todo: make this configurable
            time_plus_twenty = get_time_plus_minutes(10)

            # pull the records
            alerts = self.session.query(RescueAlert).filter(RescueAlert.adventure_end_time > datetime.now(), RescueAlert.adventure_end_time < time_plus_twenty).order_by(asc(RescueAlert.adventure_end_time)).all()

            # Essentially appending the records at the end.
            self.records[len(self.records): len(self.records)] = alerts
            for al in self.records:
                print("\t Adventure Name is {}, end-time {}".format(al.adventure_name, al.adventure_end_time))
        finally:
            self.record_list_lock.release()

    '''
    Join with all the worker threads.
    '''
    def join_worker_threads(self):
        self.record_extractor_thread.join()

        for th in self.processor_threads:
            th.join()



if __name__ == "__main__":
    print("Starting Record Processor Engine")
    rpc =  RecordProcessorCore(1)
    
    rpc.commence_engine()
    
    while("exit" != input("enter exit to quit\n")):
        print("\t Continuing to process records")

    print("joinging on threads now")
    rpc.shutdown()
    #rpc.join_worker_threads()
    print("Exiting processing")
    