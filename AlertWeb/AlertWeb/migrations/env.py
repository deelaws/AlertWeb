from __future__ import with_statement

'''
Modules are located a directory up.
Add it to your system path to access it.
'''
import sys,site
# this works for windows to add parent dir to path
site.addsitedir(sys.path[0]+'\\..\\..')  

# add path to dir for non-windows
sys.path.insert(0, '../')

print (sys.path)  # just verify it is there  

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

from AlertWeb.config import configuration
from os import environ
from AlertWeb.models import Base
from AlertWeb.mod_rescue.models import RescueAlert

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = RescueAlert.metadata

config_type = environ.get('CONFIG_TYPE', 'development')
print("Using config type {}".format(config_type))
config.set_main_option('sqlalchemy.url', configuration[config_type].SQLALCHEMY_DATABASE_URI)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
