from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from AlertWeb.mod_auth.models import User
from AlertWeb.mod_rescue.models import RescueAlert

users = ['deelaws@hotmail.com',
                'besttimothy1@gmail.com',
                'jordanb@hotmail.com',
                'deelaws89@gmail.com']


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
    query_user_alerts(session)