from flask_sqlalchemy import SQLAlchemy
from backend.models import db, bcrypt
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, Email, ValidationError
from sqlalchemy import event
import json


# User model
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
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

    # Cookbooks relationship
    cookbooks = db.relationship("Cookbook", backref="cookbook_author", lazy=True)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            "cooking_preferences": self.cooking_preferences
        }

def validate_username(form, field):
    user = User.query.filter_by(username=field.data).first()
    if form.__class__.__name__ == 'RegisterForm' and user:
        raise ValidationError("Username already exists")
    elif form.__class__.__name__ == 'LoginForm' and not user:
        raise ValidationError("Username or password is incorrect")
    
def validate_password(form, field):
    user = User.query.filter_by(username=form.username.data).first()
    if user and not user.check_password(password=field.data):
        raise ValidationError("Username or password is incorrect")

class RegisterForm(FlaskForm):

    name = StringField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Full Name"})
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20), validate_username], render_kw={"placeholder": "Username"})
    email = EmailField('Email', validators=[InputRequired(), Email()], render_kw={
                       "placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20), validate_username], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20), validate_password], render_kw={"placeholder": "Password"})
    submit = SubmitField("Log in")

# [1]
# [2]
user_json = "backend/data/users.json"
@event.listens_for(User.__table__, 'after_create')
def populate_users(mapper, connection, *args, **kwargs):
    "listen for the 'after_create' event"
    f = open(user_json)
    user_table = User.__table__
    user_json_object = json.load(f)
    for user_item in user_json_object:
        hashed_password = bcrypt.generate_password_hash(user_item["password"])
        new_user = User(
            name = user_item["name"],
            username = user_item["username"],
            email = user_item["email"],
            password = hashed_password,
            cooking_preferences = user_item["cooking_preferences"]
        )
        connection.execute(user_table.insert().values(
                                                  name=new_user.name,
                                                  username=new_user.username,
                                                  email=new_user.email,
                                                  password=new_user.password,
                                                  cooking_preferences=new_user.cooking_preferences))


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
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Ratings relationship
    ratings = db.relationship("Rating", backref="recipe", lazy=True)

    # Recipe-Cookbook relationship
    recipe_to_cookbook = db.relationship("RecipeCookbook", backref="recipe", lazy=True)

    visibility = db.Column(db.String(50), default="PUBLIC")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "visibility": self.visibility,
            "author_id": self.author_id
        }


# Rating model
class Rating(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    taste_rating = db.Column(db.Integer)
    difficulty_rating = db.Column(db.Integer)
    modification = db.Column(db.String(500))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)


# Recipe and Cookbook Model
class RecipeCookbook(db.Model):
    __tablename__ = 'recipecookbook'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    cookbook_id = db.Column(db.Integer, db.ForeignKey("cookbook.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "cookbook_id": self.cookbook_id
        }

# Cookbook model
class Cookbook(db.Model):
    __tablename__ = 'cookbook'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipes_url = db.Column(db.String(500))

    # Recipe-Cookbook relationship
    recipe_to_cookbook = db.relationship("RecipeCookbook", backref="cookbook", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author_id": self.author_id,
            "recipes_url": self.recipes_url
        }