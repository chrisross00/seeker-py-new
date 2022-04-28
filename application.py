from runmain import runmain
from flask import Flask, Blueprint
from models.base import db, migrate
from blueprints import outQuery, message, search ,searchResultDb
from flask_apscheduler import APScheduler

BLUEPRINTS = [outQuery, message, search ,searchResultDb]

## eventually need to refactor this to be a __init__ file 

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fclgfnmyyveang:6202567584b711b13678cdc116e481ef5f70f6b66ef8ebfc0e662b330d77dc32@ec2-44-199-143-43.compute-1.amazonaws.com:5432/ddes25urmoaa6i'
    app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False

    scheduler = APScheduler()
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='job_1', func=runmain, args='', trigger='interval',minutes=1)
        
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app