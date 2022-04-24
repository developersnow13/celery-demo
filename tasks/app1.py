from celery_app import celery_app


@celery_app.task(name='app1.periodic-job1', queue='clx-scheduler')
def demo01():
    print("I am periodic-job1 from app1")
