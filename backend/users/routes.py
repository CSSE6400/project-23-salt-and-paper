from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import exc
from backend.models.models import User, db, bcrypt
import json, uuid

user_api = Blueprint("user_api", __name__, url_prefix="/api/v1/users")


class UnknownFieldException(Exception):
    "Raised when there are unknown fields."

@user_api.route("/health")
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    users = User.query.all()
    if len(users) < 1:
        return jsonify({"error": "User table has not been populated."}), 500
    return jsonify({"status": "User table has been populated."}), 200


@user_api.route("/create_user", methods=["POST"])
def add_user():
    """Create a user item"""
    try:
        hashed_password = bcrypt.generate_password_hash(request.json.get("password"))
        user = User(
            name=request.json.get("name"),
            username=request.json.get("username"),
            email=request.json.get("email"),
            password=hashed_password,
            cooking_preferences = request.json.get("cooking_preferences")
        )

        if user.name == "":
            raise exc.IntegrityError

        if (
            len(
                set(request.json.keys())
                - {"name", "username", "email", "password", "cooking_preferences"}
            )
            > 0
        ):
            raise UnknownFieldException

        db.session.add(user)

        db.session.commit()
        return jsonify(user.to_dict()), 201
    
    except UnknownFieldException:
        return jsonify({"error": "There are extra fields"}), 400
    
@user_api.route('/get_all', methods=['GET'])
def get_users():
    """Return the list of user items"""
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.to_dict())
    
    return jsonify(result), 200, {'Content-Type': 'application/json'}

@user_api.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Return the details of a user item"""
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User does not exist'}), 404
    return jsonify(user.to_dict()), 200
