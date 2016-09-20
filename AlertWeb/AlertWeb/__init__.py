"""
The flask application package.
"""
import os, sys
from flask import Flask, g, session
from flask_login import LoginManager
from flask_mail import Mail, Message

from flask_sqlalchemy import SQLAlchemy
from AlertWeb.config import configuration
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy.engine import url as sqla_url

from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from alembic.runtime.environment import EnvironmentContext

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()

login_manager.login_message = 'Successful login'
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in #todo localization'


def get_current_revision(db_url):
    # create connecton
    engine = create_engine(db_url)
    connection = engine.connect()
    durl = sqla_url.make_url(db_url)
    
    mgrt_cxt = MigrationContext.configure(connection)
    #mgrt_cxt = MigrationContext(environment_context=env_cxt,
                                #connection=connection,
                                #dialect=durl.get_dialect()(),
                               # opts=None
                              #  )#
    mgrt_cxt.get_current_revision()

'''
Programattically performs database migration.
'''
def perform_migratons(config_name):
    ''' If fails, then we should revert to previous version of SLUG running on Heroku
        link: http://stackoverflow.com/questions/24622170/using-alembic-api-from-inside-application-code
    '''
    db_url = configuration[config_name].SQLALCHEMY_DATABASE_URI
    alembic_config = AlembicConfig('.\\AlertWeb\\alembic.ini')

    alembic_config.set_main_option('sqlalchemy.url', db_url)
    alembic_config.set_main_option('script_location', '.\\AlertWeb\\migrations')

    script_dir = ScriptDirectory.from_config(alembic_config)
    head_revision = script_dir.get_current_head()

    current_revision = get_current_revision(db_url)
    
    def upgrade(rev, context):
        print(rev)
        return script_dir._upgrade_revs(head_revision, rev)

    #script_dir.
    # Facade for migration context.
    with EnvironmentContext(alembic_config, 
                            script_dir,
                            as_sql=False,
                            fn=upgrade,
                            starting_rev=current_revision,
                            destination_rev=head_revision,
                            tag=None
    ):
        script_dir.run_env()

def create_app(config_name):
    app = Flask(__name__)

    # Initialize app form the specified config name
    app.config.from_object(configuration[config_name])
    configuration[config_name].init_app(app)

    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    from AlertWeb.mod_rescue.controllers import mod_resc_alert
    from AlertWeb.mod_auth.controllers import mod_auth
    from AlertWeb.mod_main import mod_main

    # Register Blueprints
    app.register_blueprint(mod_resc_alert)
    app.register_blueprint(mod_auth)
    app.register_blueprint(mod_main)

    print(app.url_map)

    @app.before_request
    def add_user_to_g():
        from AlertWeb.mod_auth.models import User
        if session.get("user_id"):
            user_obj = User.query.filter_by(email=session["user_id"]).first()
        else:
            user_obj = None #{"name": "Guest"}  # Make it better, use an anonymous User instead
        g.user = user_obj
    
    return app
