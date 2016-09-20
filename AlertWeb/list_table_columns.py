import os
from sqlalchemy import create_engine, func, inspect
from AlertWeb.config import configuration

if __name__ == "__main__":
    config_type = os.environ.get('CONFIG_TYPE', 'development')
    db_url = configuration[config_type].SQLALCHEMY_DATABASE_URI

    engine = create_engine(db_url)
    inspector = inspect(engine)
    
    for table_name in inspector.get_table_names():
        print("Table name: %s" % table_name)
        for column in inspector.get_columns(table_name):
            print("    Column: %s" % column['name'])
    