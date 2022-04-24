from celery_app import celery_app


@celery_app.task(name='app2.periodic-job1', queue='clx-scheduler')
def demo01():
    print("i am periodic-job1 from app2")
