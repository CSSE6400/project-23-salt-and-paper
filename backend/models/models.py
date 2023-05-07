from flask_sqlalchemy import SQLAlchemy
from backend.models import db


# User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(100))
    cooking_preferences = db.Column(db.String(100))

    # Followers relationship
    followers = db.relationship(
        "User",
        secondary="followers",
        primaryjoin=("User.id==followers.c.followed_id"),
        secondaryjoin=("User.id==followers.c.follower_id"),
        backref=db.backref("followed_by", lazy="dynamic"),
        lazy="dynamic",
    )

    # Recipes relationship
    recipes = db.relationship("Recipe", backref="author", lazy=True)


# Followers table
followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("users.id")),
)


# Recipe model
class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    category = db.Column(db.String(50))
    image = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Steps relationship
    steps = db.relationship("Step", backref="recipe", lazy=True)

    # Ratings relationship
    ratings = db.relationship("Rating", backref="recipe", lazy=True)

    visibility = db.Column(db.String(50), default="PUBLIC")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "image": self.image,
            "visibility": self.visibility,
            "author_id": self.author_id
        }


# Step model
class Step(db.Model):
    __tablename__ = "steps"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)


# Rating model
class Rating(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    taste_rating = db.Column(db.Integer)
    difficulty_rating = db.Column(db.Integer)
    modification = db.Column(db.String(500))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
