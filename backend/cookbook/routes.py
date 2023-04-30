from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import exc

cookbook_api = Blueprint('cookbook_api', __name__, url_prefix='/api/v1/cookbook')

@cookbook_api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})