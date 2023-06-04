from flask import Blueprint, jsonify, request, render_template
from datetime import datetime, timedelta
from sqlalchemy import exc
import uuid
from flask_wtf import csrf

from backend.models.models import Recipe, User, RecipeCookbook
from backend.models import db

recipe_api = Blueprint("recipe_api", __name__, url_prefix="/api/v1/recipe")


class UnknownFieldException(Exception):
    "Raised when there are unknown fields."


class InvalidParameterInput(Exception):
    "Raised when a parameter input is invalid."


class IDMismatchException(Exception):
    "recipe ID does not match ID in JSON object"


@recipe_api.route("/health", methods=["GET"])
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})


@recipe_api.route("/get_all", methods=["GET"])
def get_recipes():
    """Return the list of recipe items"""
    db.session.commit()
    recipes = Recipe.query.all()
    result = []
    for recipe in recipes:
        result.append(recipe.to_dict())

    return render_template('recipes.html', recipes=result)

@recipe_api.route("/get_user_recipes/<int:author_id>", methods=["GET"])
def get_user_recipes(author_id):
    """Return the list of recipe items"""
    try:
        user = User.query.get(author_id)
        if user is None:
            return jsonify({"error": "Author does not exist"}), 404

        if user.id != author_id:
            raise IDMismatchException

        recipes = Recipe.query.filter(Recipe.author_id==author_id).all()
        result = []
        for recipe in recipes:
            result.append(recipe.to_dict())

        csrf_token = csrf.generate_csrf()  # Generate CSRF token

        return render_template('recipes.html', recipes=result, csrf_token=csrf_token), 200
    
    except IDMismatchException:
        return jsonify({"error": "user ID does not match ID in JSON object"}), 400


@recipe_api.route("/create_recipe", methods=["GET"])
def view_create_recipe():
    csrf_token = csrf.generate_csrf()
    return render_template('createRecipe.html', csrf_token=csrf_token)


@recipe_api.route("/create/<int:author_id>", methods=["POST"])
def create_recipe(author_id):
    """Create a recipe item"""
    try:
        user = User.query.get(author_id)
        if user is None:
            return jsonify({"error": "Author does not exist"}), 404

        if user.id != author_id:
            raise IDMismatchException

        recipe = Recipe(
            title=request.json.get("title"),
            description=request.json.get("description"),
            category=request.json.get("category"),
            author_id=author_id,
            visibility=request.json.get("visibility"),
        )

        if recipe.visibility not in ["PUBLIC", "PRIVATE"]:
            raise InvalidParameterInput

        if not recipe.title:
            raise InvalidParameterInput

        if len(set(request.json.keys()) - {"title", "description", "category", "visibility", "csrf_token"}) > 0:
            raise UnknownFieldException

        db.session.add(recipe)
        db.session.commit()

        return jsonify(recipe.to_dict()), 201

    except exc.IntegrityError as e:
        print(str(e))
        db.session.rollback()
        return jsonify({"error": "Failed to create Recipe"}), 405

    except UnknownFieldException:
        return jsonify({"error": "There are extra fields"}), 406

    except InvalidParameterInput:
        return jsonify({"error": "Parameter input is invalid!"}), 407
    
    except IDMismatchException:
        return jsonify({"error": "recipe ID does not match ID in JSON object"}), 400



@recipe_api.route("/get_by_id/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    """Return the details of a recipe item"""
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return jsonify({"error": "recipe does not exist"}), 404
    return render_template('recipeView.html', recipe=recipe.to_dict())


@recipe_api.route("/updateRecipeView/<int:recipe_id>", methods=["GET"])
def update_recipe_view(recipe_id):
    csrf_token = csrf.generate_csrf()
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return jsonify({"error": "recipe does not exist"}), 404
    return render_template('updateRecipe.html', recipe=recipe.to_dict(), csrf_token=csrf_token)

@recipe_api.route("/update/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    """Update recipe item and return the updated recipe item"""
    # Status codes 200 (SUCCESS), 400 (INVALID PARAM), 404 (DOES NOT EXIST), 500 (UNKNOWN ERROR)
    # TODO: Implement Status Code 500 for update recipe endpoint
    try:
        recipe = Recipe.query.get(recipe_id)
        if recipe is None:
            return jsonify({"error": "recipe does not exist"}), 404

        if (
            len(
                set(request.json.keys())
                - {"title", "description", "category", "visibility", "csrf_token"}
            )
            > 0
        ):
            raise UnknownFieldException

        if request.json.get("id"):
            if recipe.id != request.json.get("id"):
                raise IDMismatchException

        recipe.title = request.json.get("title", recipe.title)
        recipe.description = request.json.get("description", recipe.description)
        recipe.category = request.json.get("category", recipe.category)
        recipe.visibility = request.json.get("visibility", recipe.visibility)

        if recipe.visibility not in ["PUBLIC", "PRIVATE"]:
            raise InvalidParameterInput

        if recipe.title == "":
            raise exc.IntegrityError

        db.session.commit()

        return jsonify(recipe.to_dict()), 200

    except UnknownFieldException:
        return jsonify({"error": "There are missing or extra fields"}), 400

    except IDMismatchException:
        return jsonify({"error": "recipe ID does not match ID in JSON object"}), 400

    except InvalidParameterInput:
        return jsonify({"error": "Parameter input is invalid!"}), 400

@recipe_api.route("/delete/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    """Delete a recipe item and return the deleted item"""
    try:
        # csrf_token = request.headers.get("X-CSRF-TOKEN")
        # if not csrf_token:
        #     return jsonify({"error": "CSRF token not found"}), 403

        # Validate the CSRF token here (e.g., using a CSRF protection library)

        recipe = Recipe.query.get(recipe_id)
        if recipe is None:
            return jsonify({"message": "Recipe does not exist"}), 200
    
        recipeCookbooks = RecipeCookbook.query.filter_by(recipe_id=recipe_id).all()

        for recipeCookbook in recipeCookbooks:
            db.session.delete(recipeCookbook)
        db.session.commit()

        db.session.delete(recipe)
        db.session.commit()
        return jsonify(recipe.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@recipe_api.route("/header", methods=["GET"])
def get_header():
    return render_template("header.html")