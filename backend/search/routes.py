from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import exc
from backend.models.models import Recipe
from backend.models import db

from sqlalchemy import or_
search_api = Blueprint('search_api', __name__, url_prefix='/api/v1/search')

@search_api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})

# def descriptioncontainKW(recipe,keywords):
#    for keyword in keywords:
#         if recipe["description"].splite().contain(keyword)
#             return True
#     return False


@search_api.route('/searchdescription/<string:keywords>') 
def searchall(keywords):
    keywordslist=keywords.split(" ")
    conditions = [Recipe.description.ilike(f'%{kw}%') for kw in keywordslist]

    # combine the conditions with 'or' operator
    filter_query = or_(*conditions)
    recipes=Recipe.query.filter(filter_query).all()
    resultlist = []
    for recipe in recipes:
        resultlist.append(recipe.to_dict())
    return jsonify(resultlist)
@search_api.route('/searchcategory/<string:keywords>') 
def searchcategory(keywords):
    # define the filter conditions
    keywordslist=keywords.split(" ")
    conditions = [Recipe.category.ilike(f'%{kw}%') for kw in keywordslist]

    # combine the conditions with 'or' operator
    filter_query = or_(*conditions)
    recipes=Recipe.query.filter(filter_query).all()
    resultlist = []
    for recipe in recipes:
        resultlist.append(recipe.to_dict())
    return jsonify(resultlist)
