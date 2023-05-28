from flask import Flask
from flask_migrate import Migrate

from backend.models import db

from backend.users.routes import user_api
from backend.auth.routes import auth_api
from backend.cookbook.routes import cookbook_api
from backend.recipe.routes import recipe_api
from backend.search.routes import search_api
from backend.models.models import User, Recipe, Step, Rating
import os


app = Flask(__name__)


db_uri = "postgresql://postgres:postgres@db:5432/saltandpaper" # using DOCKER
# db_uri = "postgresql://postgres:postgres@localhost:5432/saltandpaper" # without DOCKER

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.sort_keys = False
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()
# migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(user_api)
app.register_blueprint(auth_api)
app.register_blueprint(cookbook_api)
app.register_blueprint(recipe_api)
app.register_blueprint(search_api)


if __name__ == "__main__":
    app.run()
