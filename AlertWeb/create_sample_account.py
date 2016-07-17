from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from AlertWeb.mod_auth.models import User
from AlertWeb.mod_rescue.models import RescueAlert

users_to_add = [('deelaws@hotmail.com', 'qwqwqwqwqw'),
                ('besttimothy1@gmail.com', 'qwqwqwqwqw'),
                ('jordanb@hotmail.com', 'qwqwqwqwqw'),
                ('deelaws89@gmail.com', 'qwqwqwqwqw')]


def add_test_users_to_database(session):
    for user in users_to_add:
        print("Username: \'%s\', password: \'%s\'" % (user[0], user[1]))
        new_user = User(user[0], user[1])
        new_user.test_account = True
        session.add(new_user)

    session.commit()

if __name__ == "__main__":
    engine = create_engine('postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp')
    
    Session = sessionmaker(bind=engine)
    session = Session()
    add_test_users_to_database(session)