from flask import Blueprint, jsonify, request, render_template
from datetime import datetime, timedelta
from sqlalchemy import exc
from backend.models.models import Cookbook, db, Recipe, RecipeCookbook, User


class UnknownFieldException(Exception):
    "Raised when there are unknown fields."

class IDMismatchException(Exception):
    "recipe ID does not match ID in JSON object"

cookbook_api = Blueprint('cookbook_api', __name__, url_prefix='/api/v1/cookbook')


@cookbook_api.route('/health', methods=['GET']) 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})

@cookbook_api.route('/create_cookbook_view', methods=['GET'])
def create_cookbook_view():
    try:
        return render_template('createCookbook.html')
    except Exception as e:
        return jsonify({"error": "Failed to load page" + e}), 500

@cookbook_api.route('/create/<int:author_id>', methods=['POST'])
def create_cookbook(author_id):
    """Create a new cookbook item annd return the cookbook item"""
    # Status codes 201 (CREATE SUCCESS), 400 (INVALID PARAM), 500 (UNKNOWN ERROR)
    try:
        user = User.query.get(author_id)
        if user is None:
            return jsonify({"error": "Author does not exist"}), 404

        if user.id != author_id:
            raise IDMismatchException
        
        cookbook = Cookbook(
            title=request.json.get("title"),
            author_id = author_id
        )
        
        if cookbook.title == "":
            raise exc.IntegrityError

        if (
            len(
                set(request.json.keys())
                - {"title"}
            )
            > 0
        ):
            raise UnknownFieldException
        
        db.session.add(cookbook)
        db.session.flush()
        cookbook.recipes_url = request.url_root + "/api/v1/cookbook/get_recipes/" + str(cookbook.id)

        db.session.commit()
        return jsonify(cookbook.to_dict()), 201

    except exc.IntegrityError as e:
        print(str(e))
        db.session.rollback()
        return jsonify({"error": "Failed to create Recipe"}), 400

    except UnknownFieldException:
        return jsonify({"error": "There are extra fields"}), 400


@cookbook_api.route('/get_user_recipes/<int:author_id>', methods=['GET'])
def get_user_recipes(author_id):
    """Return a list of recipe items"""
    try:
        user = User.query.filter_by(id=author_id).first()
        if user is None:
            return jsonify({"error": "Author does not exist"}), 404
        if user.id != author_id:
            raise IDMismatchException

        recipes = Recipe.query.filter_by(author_id=author_id).all()
        result = []
        for recipe in recipes:
            result.append(recipe.to_dict())

        return render_template('cookbookAddRecipe.html', recipes=result)
    except IDMismatchException:
        return jsonify({"error": "user ID does not match ID in JSON object"}), 400
    

@cookbook_api.route('/add_recipe', methods=['POST'])
def add_recipe_to_cookbook():
    try:
        recipe_id_input = int(request.json.get("recipe_id"))
        recipe = Recipe.query.get(recipe_id_input)
        if recipe is None:
            return jsonify({"error": "Recipe does not exist"}), 404

        if recipe.id != recipe_id_input:
            raise IDMismatchException
        
        cookbook_id_input = int(request.json.get("cookbook_id"))
        cookbook = Cookbook.query.get(cookbook_id_input)
        if cookbook is None:
            return jsonify({"error": "Cookbook does not exist"}), 404
        if cookbook.id != cookbook_id_input:
            raise IDMismatchException
        
        if cookbook.author_id != recipe.author_id:
            return jsonify({"error": f"Cookbook author ({cookbook.author_id}) does not match recipe author ({recipe.author_id})."}), 400
        
        if RecipeCookbook.query.filter_by(recipe_id=recipe_id_input, cookbook_id=cookbook_id_input).first():
            return jsonify({"success": "Recipe already exists in cookbook"}), 201 #Recipe already exist in cookbook
        
        recipeCookbook = RecipeCookbook(
            recipe_id = recipe_id_input,
            cookbook_id = cookbook_id_input
        )

        if len(set(request.json.keys()) - {'recipe_id', 'cookbook_id'}) > 0:
            raise UnknownFieldException
        
        db.session.add(recipeCookbook)
        db.session.commit()
        return jsonify(recipeCookbook.to_dict()), 201
        
    except UnknownFieldException:
        return jsonify({"error": "There are extra fields"}), 400
    
    except IDMismatchException:
        return jsonify({"error": "recipe ID does not match ID in JSON object"}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cookbook_api.route('/get_recipes/<int:cookbook_id>', methods=['GET'])
def get_recipes(cookbook_id):
    """Return all recipe items in cookbook"""
    try:
        cookbook = Cookbook.query.get(cookbook_id)
        if cookbook is None:
            return jsonify({"error": "Cookbook does not exist"}), 404
        if cookbook.id != cookbook_id:
            raise IDMismatchException
        
        recipes = db.session.query(RecipeCookbook, Recipe)\
                    .filter(RecipeCookbook.cookbook_id==cookbook_id)\
                    .join(Recipe, RecipeCookbook.recipe_id==Recipe.id).all()
        
        result = []
        for _, recipe in recipes:
            print(recipe)
            result.append(recipe.to_dict())
        
        return render_template('cookbookRecipes.html', recipes=result)
    
    except IDMismatchException:
        return jsonify({"error": "recipe ID does not match ID in JSON object"}), 400
    
    except Exception as e:
        print(e)
        return jsonify({'error': e}), 500



@cookbook_api.route('/get_user_cookbooks/<int:author_id>', methods=['GET'])
def get_cookbooks(author_id):
    """"Return all cookbook items"""
    try:
        user = User.query.get(author_id)
        if user is None:
            return jsonify({"error": "Author does not exist"}), 404

        if user.id != author_id:
            raise IDMismatchException
        cookbooks = Cookbook.query.filter(Cookbook.author_id==author_id).all()
        result = []
        for cookbook in cookbooks:
            result.append(cookbook.to_dict())
        
        return render_template('viewCookBooks.html', cookbooks=result)

    except IDMismatchException: 
        return jsonify({"error": "recipe ID does not match ID in JSON object"}), 400
    
    except Exception as e:
        print(e)
        return jsonify({'error': e}), 500
    
@cookbook_api.route('/get_cookbook/<int:cookbook_id>', methods=['GET'])
def get_cookbook(cookbook_id):
    """"Return cookbook item of a user"""
    try:
        cookbook = Cookbook.query.get(cookbook_id)
        if cookbook is None:
            return jsonify({"error": "Cookbook does not exist"}), 404
        if cookbook.id != cookbook_id:
            raise IDMismatchException
        
        cookbook = Cookbook.query.filter(Cookbook.id==cookbook_id).all()
        
        return jsonify(cookbook), 200, {'Content-Type': 'application/json'}

    except IDMismatchException:
        return jsonify({"error": "recipe ID does not match ID in JSON object"}), 400
    
    except Exception as e:
        print(e)
        return jsonify({'error': e}), 500
    


