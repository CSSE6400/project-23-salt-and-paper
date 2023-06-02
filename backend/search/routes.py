from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import exc
from backend.models.models import Recipe
from backend.models import db

from celery.result import AsyncResult
import time
from sqlalchemy import or_
search_api = Blueprint('search_api', __name__, url_prefix='/api/v1/search')

@search_api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})

@search_api.route('/searchcategory/<string:keywords>') 
def searchCategory(keywords):
    docs = Recipe.query.all()
    doc = [doc.to_dict() for doc in docs]
    task = searchCatOrDes.delay(doc, keywords, True)
    while True:
        if task.ready():
            task_result = task.result 
            return task_result, 200
        else:
            time.sleep(1)

@search_api.route('/searchdescription/<string:keywords>') 
def searchDescription(keywords):
    docs = Recipe.query.all()
    doc = [doc.to_dict() for doc in docs]
    task = searchCatOrDes.delay(doc, keywords, False)
    while True:
        if task.ready():
            task_result = task.result
            return task_result, 200
        else:
            time.sleep(1)
