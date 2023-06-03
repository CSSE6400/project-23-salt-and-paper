from flask import Flask
from flask_migrate import Migrate
import json

from backend.models import db

from backend.users.routes import user_api
from backend.auth.routes import auth_api
from backend.cookbook.routes import cookbook_api
from backend.recipe.routes import recipe_api
from backend.search.routes import search_api
from backend.models.models import User, Recipe, Rating
import os


app = Flask(__name__, template_folder="/frontend/templates/")

# CSRF  Protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

db_uri = "postgresql://postgres:postgres@db:5432/saltandpaper" # using DOCKER
# db_uri = "postgresql://postgres:postgres@localhost:5432/saltandpaper" # without DOCKER

# app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.sort_keys = False
db.init_app(app)

csrf.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    
# Load recipe data from JSON file
# with open("recipes.json") as f:
#     dummy_recipes = json.load(f)

# # Populate the Recipe table
# try:
#     with app.app_context():
#         for recipe_data in dummy_recipes:
#             new_recipe = Recipe(
#                 id=recipe_data['id'],
#                 title=recipe_data['title'],
#                 description=recipe_data['description'],
#                 category=recipe_data['category'],
#                 visibility=recipe_data['visibility'],
#                 author_id=recipe_data['author_id']
#             )
#             db.session.add(new_recipe)
#         db.session.commit()
# except Exception as e:
#     print(f"Error populating Recipe table: {e}")


# Load rating data from JSON file
# with open("ratings.json") as f:
#     dummy_ratings = json.load(f)

# # Populate the Rating table
# try:
#     with app.app_context():
#         for rating_data in dummy_ratings:
#             new_rating = Rating(
#                 id=rating_data['id'],
#                 taste_rating=rating_data['taste_rating'],
#                 difficulty_rating=rating_data['difficulty_rating'],
#                 modification=rating_data['modification'],
#                 recipe_id=rating_data['recipe_id']
#             )
#             db.session.add(new_rating)
#         db.session.commit()
# except Exception as e:
#     print(f"Error populating Rating table: {e}")
# migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(user_api)
app.register_blueprint(auth_api)
app.register_blueprint(cookbook_api)
app.register_blueprint(recipe_api)
app.register_blueprint(search_api)


if __name__ == "__main__":
   app.run(ssl_context='adhoc')
