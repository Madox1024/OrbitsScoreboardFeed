import os
import time

from AbnormalLapCheck import start_abnormal_lap_check
from DriverStintCheck import start_driver_stint_check
from LeaderBoardFeed import start_leader_board_feed


def lap_times_mod_time(file_name, tries_count):
    if tries_count > 5:
        print('Cannot find file, please restart')
        start_race(is_restart())
    try:
        result = os.path.getmtime(file_name)
        return result
    except FileNotFoundError:
        print('Waiting for {filename} export...'.format(filename=file_name))
        tries_count += 1
        time.sleep(2)
        return lap_times_mod_time(file_name, tries_count)


def start_monitors(restart):
    print('Initiating Monitors')
    start_driver_stint_check(restart)
    start_leader_board_feed()
    start_abnormal_lap_check()
    #  how can I start all 3 of these threads, currently it hangs on the first WT loop


def is_restart():
    restart_input = input('Has the race started? Y/N: ')
    if restart_input.upper() == 'Y':
        return True
    elif restart_input.upper() == 'N':
        return False
    else:
        print('Invalid Input \nPlease enter either "Y" (Yes) or "N" (No)')
        is_restart()


csv_file_name = ''


def ask_file_name():
    global csv_file_name
    csv_file_name = input('Input LapTimes.csv file name w/ extension (Do not export yet!): ')
    return csv_file_name


def start_race(restart):
    if restart:
        file_name = ask_file_name()
        print('Export {filename} now'.format(filename=file_name))
        if lap_times_mod_time(file_name, 0) - time.time() < 3:
            start_monitors(restart)
        else:
            print("Something went wrong, please restart")
    else:
        start_monitors(restart)


start_race((is_restart()))
