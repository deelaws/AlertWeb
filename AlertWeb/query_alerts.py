from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
from AlertWeb.mod_auth.models import User
from AlertWeb.mod_rescue.models import RescueAlert
from datetime import datetime, timedelta
from time import sleep
from math import log10

def get_time_plus_minutes(min):
    now = datetime.now()
    print("Now = {}".format(now))
    now_plus_min = now + timedelta(minutes=min)
    print("{} minutes from now = {}".format(min, now_plus_min))
    return now_plus_min

def query_user_alerts(session):
    for user in session.query(User):
        print(user.email)
        for alert in user.rescue_alerts:
            print("\t Name: {}".format(alert.adventure_name))
            print("\t Start time: {}".format(alert.adventure_start_time))


if __name__ == "__main__":
    engine = create_engine('postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp')
    
    Session = sessionmaker(bind=engine)
    session = Session()

    time_plus_twenty = get_time_plus_minutes(5)
    alerts = session.query(RescueAlert).filter(RescueAlert.adventure_end_time > datetime.now(), \
                                               RescueAlert.adventure_end_time < time_plus_twenty ).order_by(asc(RescueAlert.adventure_end_time))
    for al in alerts:
        print("Alerts endtime {}".format(al.adventure_end_time))
        
        #time_delta =  datetime.now() - al.adventure_end_time
        
        time_delta = al.adventure_end_time - datetime.now()
        print(time_delta.days < 0)
        