from runmain import runmain
from flask import Flask, Blueprint
from models.base import db, migrate
from blueprints import query, message, search ,searchResultDb
from flask_apscheduler import APScheduler

BLUEPRINTS = [query, message, search ,searchResultDb]

## eventually need to refactor this to be a __init__ file 
# ## https://www.youtube.com/watch?v=WhwU1-DLeVw
# ## https://github.com/PrettyPrinted/youtube_video_code/tree/master/2022/02/02/How%20to%20Use%20Flask-SQLAlchemy%20With%20Flask%20Blueprints/sqlalchemy_blueprint/myproject/

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False

    
    #not sure if this should be on application.py or server.py...
    scheduler = APScheduler()
    scheduler.api_enabled = True

    with app.app_context():
        scheduler.init_app(app)
        scheduler.start()
        scheduler.add_job(id='job_1', func=runmain, args='', trigger='interval',seconds=20)
        
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app