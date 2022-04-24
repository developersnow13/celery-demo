from datetime import timedelta

beat_schedule = {
    'periodic-job1': {
        'task': 'app1.periodic-job1',
        'schedule': timedelta(seconds=5)
    }
}