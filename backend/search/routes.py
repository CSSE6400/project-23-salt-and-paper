from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import exc
from backend.models.models import Recipe
from backend.models import db

from celery.result import AsyncResult
from backend.search.searchservice import updateBM25_cat,updateBM25_des
import time
from sqlalchemy import or_


import nltk
from nltk.stem import PorterStemmer
from rank_bm25 import BM25Okapi

global Documents 
Documents= []
global DocumentsExpiretime 
DocumentsExpiretime= time.time()
global BM25_des 
BM25_des= None
global BM25_cat 
BM25_cat = None
global BM25_destaskid 
BM25_destaskid= None
global BM25_cattaskid 
BM25_cattaskid= None
global BM25_desExpiretime 
BM25_desExpiretime = time.time()
global BM25_catExpiretime 
BM25_catExpiretime = time.time()
global desrequested
desrequested=False
global catrequested
catrequested=False

search_api = Blueprint('search_api', __name__, url_prefix='/api/v1/search')

@search_api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})



@search_api.route('/searchdescription/?keyword=<string:keywords>') 
def searchall(keywords):
    keywordslist=keywords.split("&")
    conditions = [Recipe.description.ilike(f'%{kw}%') for kw in keywordslist]

    # combine the conditions with 'or' operator
    filter_query = or_(*conditions)
    recipes=Recipe.query.filter(filter_query).all()
    resultlist = []
    for recipe in recipes:
        resultlist.append(recipe.to_dict())
    return jsonify(resultlist)



def preprocess(text):
    nltk.download('punkt') # This downloads the necessary files for tokenization
    nltk.download('wordnet') 
    nltk.download('stopwords')
    porter = PorterStemmer() 
    tokens = nltk.word_tokenize(text.lower())
    stemmed_tokens = [porter.stem(token) for token in tokens]
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_tokens = [token for token in stemmed_tokens if token not in stop_words]
    return filtered_tokens

@search_api.route('/searchcatergory/?keyword=<string:keywords>') 
def searchcategory(keywords):
    # define the filter conditions
    keywordslist=keywords.split("&")
    conditions = [Recipe.category.ilike(f'%{kw}%') for kw in keywordslist]

    # combine the conditions with 'or' operator
    filter_query = or_(*conditions)
    recipes=Recipe.query.filter(filter_query).all()
    resultlist = []
    for recipe in recipes:
        resultlist.append(recipe.to_dict())
    return jsonify(resultlist)

def searchquery(Recipedoc,bm25,query, n=5):
    preprocessed_query = preprocess(query)
    scores = bm25.get_scores(preprocessed_query)
    sorted_indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    top_indexes = sorted_indexes[:n]
    return [Recipedoc[i] for i in top_indexes]

@search_api.route('/searchcategory/<string:keywords>') 
def searchCatergory(keywords):
    global Documents
    global DocumentsExpiretime
    global BM25_catExpiretime
    global BM25_cattask
    global BM25_cat
    global catrequested
    if time.time() > DocumentsExpiretime:
        Documents=Recipe.query.all()
        Documents=[doc.to_dict() for doc in Documents]
        DocumentsExpiretime=time.time()+300

    if time.time() >  BM25_catExpiretime :
        if BM25_cat!=None:#  store file exist
            if not catrequested: # did not send request
                BM25_cattask= updateBM25_cat.delay(Documents)
                catrequested=True
            if  BM25_cattask.ready() and catrequested:
                    #get acsy result
                    BM25_cat=BM25Okapi(AsyncResult(BM25_cattask.id).result)
                    BM25_catExpiretime=time.time()+300
                    catrequested=False
            # else:# not ready use stored 
             
        else :# BM25_cattaskid==None wait for result
                BM25_cattask= updateBM25_cat.delay(Documents)
                while(True):
                    if BM25_cattask.ready():
                              #get acsy result
                        BM25_cat=BM25Okapi(AsyncResult(BM25_cattask.id).result)
                        BM25_catExpiretime=time.time()+300
                        break
                    else:
                        time.sleep(1)
    return searchquery(Documents,BM25_cat,keywords)



@search_api.route('/searchdescription/<string:keywords>') 
def searchDescription(keywords):
    global DocumentsExpiretime
    global BM25_desExpiretime
    global BM25_destask
    global BM25_des
    global desrequested
    global Documents
    if time.time() > DocumentsExpiretime:
        Documents=Recipe.query.all()
        Documents=[doc.to_dict() for doc in Documents]
        DocumentsExpiretime=time.time()+300
   
    if time.time() >  BM25_desExpiretime:
        if BM25_des!=None:#  store file exist
            if not desrequested:
                BM25_destask= updateBM25_des.delay(Documents)
                requested=True
            if  BM25_destask.ready() and requested:
                    #get acsy result
                    BM25_des=BM25Okapi(AsyncResult(BM25_destask.id).result)
                    BM25_desExpiretime=time.time()+300
                    
            # else:# not ready use stored 
             
        else :# BM25_destaskid==None
                BM25_destask= updateBM25_des.delay(Documents)
                while(True):
                    if BM25_destask.ready():
                              #get acsy result
                         
                        BM25_des=BM25Okapi(AsyncResult(BM25_destask.id).result)
                        BM25_desExpiretime=time.time()+300
                        break
                    else:
                        time.sleep(1)

    return searchquery(Documents,BM25_des,keywords)
