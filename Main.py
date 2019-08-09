import os


def lap_times_mod_time():
    result = os.path.getmtime('TestLapTimes.csv')
    return result
