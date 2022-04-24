'''
Celery app for task management
'''
import os
from celery import Celery

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
celery_app = Celery('celery-app',
                    backend='rpc://',
                    broker="pyamqp://guest@localhost//")

celery_app.config_from_object('celery_main_config')