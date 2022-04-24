from celery_app import celery_app


@celery_app.task(name='app3.periodic-job1', queue='clx-scheduler')
def demo01():
    import time
    time.sleep(2)
    print("i am periodic-job1 from app3")