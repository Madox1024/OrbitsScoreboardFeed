import os
import time

from AbnormalLapCheck import start_abnormal_lap_check, instantiate_team_lap_check
from DriverStintCheck import start_driver_stint_check, start_dsc_instantiation


def lap_times_mod_time(file_name, tries_count):
    if tries_count > 30:
        print('Cannot find file, please make sure that the file is named exactly "CurrentPassings.csv" \nRestarting')
        start_race(is_restart())
    try:
        result = os.path.getmtime(file_name)
        return result
    except FileNotFoundError:
        if tries_count % 5 == 0:
            print('Waiting for {filename} export...'.format(filename=file_name))
        tries_count += 1
        time.sleep(2)
        return lap_times_mod_time(file_name, tries_count)


def start_monitors(restart):
    print('Populating Driver Info')
    driver_stint_dict = start_dsc_instantiation(restart)
    abnormal_lap_dict = instantiate_team_lap_check()
    print('Initiating Monitors')
    while True:
        start_driver_stint_check(driver_stint_dict)
        start_abnormal_lap_check(abnormal_lap_dict)
        #  add leaderboard feed


def is_restart():
    restart_input = input('Has the race started? Y/N: ')
    if restart_input.upper() == 'Y':
        return True
    elif restart_input.upper() == 'N':
        return False
    else:
        print('Invalid Input \nPlease enter either "Y" (Yes) or "N" (No)')
        return is_restart()


def start_race(restart):
    if restart:
        file_name = 'CurrentPassings.csv'
        print('Please export a passings csv and name it EXACTLY: "{filename}"'.format(filename=file_name))
        time.sleep(2)
        print('You have 1 Minute'.format(filename=file_name))
        if abs(lap_times_mod_time(file_name, 0) - time.time()) < 3:
            print('Export Found!')
            time.sleep(1)
            start_monitors(restart)
        else:
            print("{filename} is too old. Deleting {filename}, wait for prompt to export".format(filename=file_name))
            os.remove(file_name)
            print('Restarting Program')
            start_race((is_restart()))
    else:
        start_monitors(restart)


start_race((is_restart()))
