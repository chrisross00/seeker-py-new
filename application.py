import os
from runmain import runmain
from flask import Flask, Blueprint
from models.base import db, migrate
from blueprints import outQuery, message, search ,searchResultDb, searchParameters
from flask_apscheduler import APScheduler

BLUEPRINTS = [outQuery, message, search ,searchResultDb, searchParameters]

## eventually need to refactor this to be a __init__ file 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('CSRF_SECRET_KEY', None)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', None)
    app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQL_ALCHEMY_TRACK_MODIFICATIONS', None)

    scheduler = APScheduler()
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='job_1', func=runmain, args='', trigger='interval',minutes=2)
    print('starting job_1...')
        
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app