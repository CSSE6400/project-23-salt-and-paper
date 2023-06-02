from flask import Blueprint, jsonify
from backend.tasks.async_task import async_health

search_api = Blueprint('search_api', __name__, url_prefix='/api/v1/search')

from celery import Celery

celery = Celery(
    'backend',
    broker='redis://redis:6379',
    backend='redis://redis:6379'
)

# Import your tasks here
from backend.tasks.async_task import async_health

@search_api.route('/health')
def health():
    try:
        task = async_health.delay()
        result = task.get()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Ticket not found"}), 801

@search_api.route('/searchcategory/<string:keywords>')
def searchKeyword(keywords):
    pass

if __name__ == '__main__':
    celery.start()
