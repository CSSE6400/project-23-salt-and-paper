from flask import Flask
from src.backend.users.models import db

from src.backend.users.routes import user_api
from src.backend.auth.routes import auth_api
from src.backend.cookbook.routes import cookbook_api
from src.backend.recipe.routes import recipe_api
from src.backend.search.routes import search_api


def create_app(config_overrides=None):
    app = Flask(__name__)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_BINDS = {
            'cookbook': 'sqlite:///cookbook-db.sqlite',
            'recipe': 'sqlite:///recipe-db.sqlite',
            'users': 'sqlite:///users-db.sqlite'
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
    if config_overrides:
        app.config.update((config_overrides))

    
    db.init_app(app)
    # Create db tables
    with app.app_context():
        db.create_all()
        db.session.commit()

    # Register blueprints
    app.register_blueprint(user_api)
    app.register_blueprint(auth_api)
    app.register_blueprint(cookbook_api)
    app.register_blueprint(recipe_api)
    app.register_blueprint(search_api)


    return app