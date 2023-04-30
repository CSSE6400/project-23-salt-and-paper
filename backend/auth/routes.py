from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import exc

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/v1/auth')

@auth_api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})