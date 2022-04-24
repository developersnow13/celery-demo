import importlib
from os import walk

TASKS = 'tasks'
ADDITIONAL_CONFIGS = 'conf'

def get_includes():
    # hat reads all of the file names in tasks folder and create a tuple of file paths
    f = []
    for (dirpath, dirnames, filenames) in walk(TASKS):
        f = [f"{TASKS}.{x.split('.')[0]}" for x in filenames]
        break
    return tuple(f)

def get_beat_schedules():
    beat_schedule = dict()
    for (dirpath, dirnames, filenames) in walk(ADDITIONAL_CONFIGS):
        f = [x.split('.')[0] for x in filenames]
        for file in f:
            if file not in '__init__':
                a = importlib.import_module(f"{ADDITIONAL_CONFIGS}.{file}")
                try:
                    schedules = a.beat_schedule
                    for key, value in schedules.items():
                        beat_schedule[f"{file}.{key}"] = value
                except AttributeError as e:
                    print(e)
        break
    return beat_schedule

if __name__ == '__main__':
    print(get_beat_schedules())
