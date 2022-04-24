from datetime import timedelta

beat_schedule = {
    'periodic-job1': {
        'task': 'app3.periodic-job1',
        'schedule': timedelta(seconds=2)
    },
}