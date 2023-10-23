from flask import Flask 
from emailing_system.extensions import db, scheduler
from flask_cors import CORS
from emailing_system.routes import email_system_blueprints
from emailing_system.create_dummy_data import create_tables
import logging
logging.basicConfig(
    # filename='record.log', 
    level=logging.INFO
)
def create_app(CREATE_DATABASE = False):
    app = Flask('AUTO_EMAIL_BOT')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.sqlite3'
    # app.config.from_object(config_object)
    app = register_blueprints(app)
    register_extensions(app)
    cors = CORS(app)
    if CREATE_DATABASE:
        create_tables(app)
    return app

def register_extensions(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    scheduler.init_app(app)
    with app.app_context():
        scheduler.start()

def register_blueprints(app):
    with app.app_context():
        app.register_blueprint(email_system_blueprints)
    return app