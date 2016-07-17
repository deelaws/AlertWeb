from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy import func
from sys import argv
from random import randint
from sqlalchemy.orm import sessionmaker
from AlertWeb.mod_auth.models import User
from AlertWeb.mod_rescue.models import RescueAlert
from AlertWeb.mod_rescue.adventure_type import AdventureType

ralert_to_add = [('Yosemite', AdventureType.Hike.value, 'deelaws@hotmail.com'),
                ('Lake Tahoe', AdventureType.SnowBoarding.value, 'besttimothy1@gmail.com'),
                ('Lake Ontario', AdventureType.Kayaking.value, 'jordanb@hotmail.com'),
                ('Denali National Park', AdventureType.BackCounntry.value, 'deelaws89@gmail.com')]


def add_ralert_to_to_database(session):
    for adven in ralert_to_add:
        print("Adventure Name: \'%s\', Type: \'%d\'" % (adven[0], adven[1]))
        new_alert = RescueAlert(adven[0],adven[1], func.current_timestamp(), func.current_timestamp())
        user = session.query(User).filter_by(email=adven[2]).first()
        user.rescue_alerts.append(new_alert)
        session.add(user)

    session.commit()

def get_time_plus_minutes(min):
    now = datetime.now()
    print("Now = {}".format(now))
    now_plus_min = now + timedelta(minutes=min)
    print("One hour from now = {}".format(now_plus_min))
    return now_plus_min

def get_time_half_hour_from_now():
    return get_time_plus_minutes(30)

def get_time_one_hour_from_now():
    now = datetime.now()
    print("Now = {}".format(now))
    now_plus_one = now.replace(hour=now.hour+1)
    print("One hour from now = {}".format(now_plus_one))
    return now_plus_one

def play_with_time(session, name):
    user = session.query(User).filter_by(email='jordanb@hotmail.com').first()

    new_alert = RescueAlert(name, 
                            AdventureType.SnowBoarding.value, 
                            func.current_timestamp(), 
                            get_time_plus_minutes(30))
                            #func.current_timestamp().op('AT TIME ZONE')('UTC'))
                            #func.current_timestamp())
    user.rescue_alerts.append(new_alert)
    session.add(user)
    session.commit()



def generate_random_alerts(session, num):
    users = session.query(User).all()
    num_users = len(users)
    print("Number of users {}.".format(num_users))

    for i in range(0,num):
        # pick random user
        user_num = randint(0,num_users-1)

        adven_name = "yosemite" + str(i)
        # create the alert
        new_alert = RescueAlert(adven_name, 
                            AdventureType.SnowBoarding.value, 
                            func.current_timestamp(), 
                            get_time_plus_minutes(randint(0,60)))
        users[user_num].rescue_alerts.append(new_alert)
    
    for user in users:
        session.add(user)
    session.commit()



if __name__ == "__main__":
    engine = create_engine('postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp')
   
    Session = sessionmaker(bind=engine)
    session = Session()
    generate_random_alerts(session, 20)