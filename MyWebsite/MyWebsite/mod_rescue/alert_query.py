#!"C:\Users\washahid\documents\visual studio 2015\Projects\MyWebsite\MyWebsite\MyWebEnv\Scripts\python.exe"

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

if __name__ == "__main__":
    print("Querying all rescue alerts") 
    connection = engine.connect()
    result = connection.execute("select * from rescue_alert")
    for row in result:
        print("alert_name", row['adventure_name'])

    connection.close()