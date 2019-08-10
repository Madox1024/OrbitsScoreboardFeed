import os

from AbnormalLapCheck import start_abnormal_lap_check
from DriverStintCheck import start_driver_stint_check
from LeaderBoardFeed import start_leader_board_feed


def lap_times_mod_time():
    result = os.path.getmtime('TestLapTimes.csv')
    return result


def start_monitors():
    start_driver_stint_check(True)
    start_leader_board_feed()
    start_abnormal_lap_check()

start_monitors()