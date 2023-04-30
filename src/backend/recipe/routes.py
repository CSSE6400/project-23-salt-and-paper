from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import exc

recipe_api = Blueprint('recipe_api', __name__, url_prefix='/api/v1/recipe')

@recipe_api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})