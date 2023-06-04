#[11]
#[13]
#[14]
import nltk
from nltk.stem import PorterStemmer
from rank_bm25 import BM25Okapi

import os
from celery import Celery
celery = Celery(__name__)

# celery.conf.broker_url = redis://redis:6379
# celery.conf.result_backend= redis://redis:6379
celery.conf.sqlalchemy_database_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery.conf.task_default_queue = os.environ.get("CELERY_DEFAULT_QUEUE", "search")

def preprocess(text):
    porter = PorterStemmer() 
    tokens = nltk.word_tokenize(text.lower())
    stemmed_tokens = [porter.stem(token) for token in tokens]
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_tokens = [token for token in stemmed_tokens if token not in stop_words]
    return filtered_tokens

def searchquery(Recipedoc,bm25,query, n=5):
    preprocessed_query = preprocess(query)
    scores = bm25.get_scores(preprocessed_query)
    sorted_indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    top_indexes = sorted_indexes[:n]
    return [Recipedoc[i] for i in top_indexes]

@celery.task(name="search")
def searchCatOrDes(Recipedoc,keywords,category):
    nltk.download('punkt') # This downloads the necessary files for tokenization
    nltk.download('wordnet') 
    nltk.download('stopwords')
    if category:
        preprocessed = [preprocess(doc["category"]) for doc in Recipedoc]
    else:
        preprocessed = [preprocess(doc["description"]) for doc in Recipedoc]
   
    bm25= BM25Okapi(preprocessed)
    return searchquery(Recipedoc,bm25,keywords) 

@celery.task
def add(x, y):
    result = x + y
    # Update the result in the backend
    return result
