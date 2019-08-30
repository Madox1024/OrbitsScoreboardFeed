import os
import time

from AbnormalLapCheck import start_abnormal_lap_check, instantiate_team_lap_check
from DriverStintCheck import start_driver_stint_check, start_dsc_instantiation
from Util import log_print


def lap_times_mod_time(file_name, tries_count):
    if tries_count > 30:
        log_print('Cannot find file, please make sure that the file is named exactly "CurrentPassings.csv" \nRestarting')
        start_race(is_restart())
    try:
        result = os.path.getmtime(file_name)
        return result
    except FileNotFoundError:
        if tries_count % 5 == 0:
            log_print('Waiting for {filename} export...'.format(filename=file_name))
        tries_count += 1
        time.sleep(2)
        return lap_times_mod_time(file_name, tries_count)


def start_monitors(restart):
    driver_info_msg = 'Populating Driver Info'
    log_print(driver_info_msg)
    driver_stint_dict = start_dsc_instantiation(restart)
    abnormal_lap_dict = instantiate_team_lap_check()
    initiating_monitors = 'Initiating Monitors {timestamp}'.format(timestamp=time.ctime(time.time()))
    log_print(initiating_monitors)
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
        log_print('Invalid Input \nPlease enter either "Y" (Yes) or "N" (No)')
        return is_restart()


def start_race(restart):
    if restart:
        file_name = 'CurrentPassings.csv'
        log_print('Please export a passings csv and name it EXACTLY: "{filename}"'.format(filename=file_name))
        time.sleep(2)
        log_print('You have 1 Minute'.format(filename=file_name))
        if abs(lap_times_mod_time(file_name, 0) - time.time()) < 3:
            export_found = 'Export Found!'
            log_print(export_found)
            time.sleep(2)
            start_monitors(restart)
        else:
            log_print("{filename} is too old. Deleting {filename}, wait for prompt to export".format(filename=file_name))
            os.remove(file_name)
            start_race(restart)
    else:
        start_monitors(restart)


start_race((is_restart()))
