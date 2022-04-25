from flask import Flask, Blueprint
from models.base import db, migrate
from blueprints import query, message, search ,searchResultDb

BLUEPRINTS = [query, message, search ,searchResultDb]

## eventually need to refactor this to be a __init__ file https://www.youtube.com/watch?v=WhwU1-DLeVw

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app

# flask db init
# flask db migrate
# flask db upgrade