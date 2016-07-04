from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from MyWebsite.mod_auth.models import User
from MyWebsite.mod_rescue.models import RescueAlert

engine = create_engine('postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp')

#connection = engine.connect()

Session = sessionmaker(bind=engine)

session = Session()

new_user = User("deelaws@hotmail.com", "qwqwqwqwqw")

session.add(new_user)

session.commit()