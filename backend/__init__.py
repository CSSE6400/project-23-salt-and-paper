from flask import Flask
from flask_migrate import Migrate

from backend.users.models import db

from backend.users.routes import user_api
from backend.auth.routes import auth_api
from backend.cookbook.routes import cookbook_api
from backend.recipe.routes import recipe_api
from backend.search.routes import search_api
from backend.users.models.models import User, Recipe, Step, Rating



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/saltandpaper"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(user_api)
app.register_blueprint(auth_api)
app.register_blueprint(cookbook_api)
app.register_blueprint(recipe_api)
app.register_blueprint(search_api)



if __name__ == "__main__":
    app.run()
