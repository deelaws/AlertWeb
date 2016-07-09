from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from MyWebsite.mod_auth.models import User
from MyWebsite.mod_rescue.models import RescueAlert
from MyWebsite.mod_rescue.adventure_type import AdventureType

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

if __name__ == "__main__":
    engine = create_engine('postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp')
    
    Session = sessionmaker(bind=engine)
    session = Session()
    add_ralert_to_to_database(session)