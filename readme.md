###Installation
pip install celery flower

###backend
rabbitmq

###Start beat
celery -A celery_app beat --loglevel=info

###Start worker
celery -A celery_app worker --loglevel=info -n clx-scheduler-W1@%%h -Q clx-scheduler

###start flower
celery -A celery_app flower --port=5566 --conf=flowerconfig.py