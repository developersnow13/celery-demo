from celery_utilities import get_includes, get_beat_schedules

broker_connection_timeout = 7800
broker_heartbeat = 7800

# Set broker pool limit to zero
broker_pool_limit = 0

# Broker transport option to allow celery publisher to timeout and retry if Broker is unavailable
broker_transport_options = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}

include = get_includes()

beat_schedule = get_beat_schedules()

worker_concurrency = 4
beat_max_loop_interval = 30
timezone = 'US/Eastern'
