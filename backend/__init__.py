from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
import json

from backend.models import db, bcrypt

from backend.users.routes import user_api
from backend.auth.routes import auth_api
from backend.cookbook.routes import cookbook_api
from backend.recipe.routes import recipe_api
from backend.search.routes import search_api
from backend.models.models import User, RegisterForm, LoginForm, Recipe, Rating
import os

app = Flask(__name__, template_folder="/frontend/templates/")


db_uri = "postgresql://postgres:postgres@db:5432/saltandpaper" # using DOCKER
# db_uri = "postgresql://postgres:postgres@localhost:5432/saltandpaper" # without DOCKER

# app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.sort_keys = False
app.config['SECRET_KEY'] = 'any secret string'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_api.login"

db.init_app(app)
bcrypt.init_app(app)
with app.app_context():
    # db.drop_all()
    db.create_all()
    
# migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(user_api)
app.register_blueprint(auth_api)
app.register_blueprint(cookbook_api)
app.register_blueprint(recipe_api)
app.register_blueprint(search_api)

@app.route("/")
def home():
    return render_template("index.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run()
