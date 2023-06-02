import os
from flask import jsonify
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery.conf.task_default_queue = os.environ.get(
    "CELERY_DEFAULT_QUEUE", "async_exec")


@celery.task(name="async_exec")
def print_async_ticket():
    return jsonify({"status": "ok"})