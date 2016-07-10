﻿from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from MyWebsite.mod_auth.models import User
from MyWebsite.mod_rescue.models import RescueAlert
from datetime import datetime, timedelta

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

    time_plus_twenty = get_time_plus_minutes(20)
    alerts = session.query(RescueAlert).filter(RescueAlert.adventure_end_time > datetime.now(), RescueAlert.adventure_end_time < time_plus_twenty )
    for al in alerts:
        print("Alerts endtime {}".format(al.adventure_end_time))