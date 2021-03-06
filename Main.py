import os
import time

from AbnormalLapCheck import start_abnormal_lap_check, instantiate_team_lap_check
from DriverStintCheck import start_driver_stint_check, start_dsc_instantiation
from Util import log_print


class Startup:

    def __init__(self):
        self.restart = self.get_restart()

        class TeamDicts:
            def __init__(self, restart, passings_file_name):
                log_print('Populating Driver Info')
                self.driver_stint_dict = start_dsc_instantiation(restart, passings_file_name)
                self.abnormal_lap_dict = instantiate_team_lap_check()

        if self.restart:
            self.passings_file_name = input("Please enter the name of the passings.csv file export "
                                            "(Don't export yet): ")
            self.get_passings_export()
            self.team_dicts = TeamDicts(self.restart, self.passings_file_name)
            self.driver_stint_dict = self.team_dicts.driver_stint_dict
            self.abnormal_lap_dict = self.team_dicts.abnormal_lap_dict
            self.start_monitors()
        else:
            self.passings_file_name = 'N/A'
            self.team_dicts = TeamDicts(self.restart, self.passings_file_name)
            self.driver_stint_dict = self.team_dicts.driver_stint_dict
            self.abnormal_lap_dict = self.team_dicts.abnormal_lap_dict
            self.start_monitors()

    def get_restart(self):
        restart_input = (input('Has the race started? Y/N: ')).upper()
        if restart_input == 'Y':
            return True
        elif restart_input == 'N':
            return False
        else:
            log_print('Invalid Input \nPlease enter either "Y" (Yes) or "N" (No)')
            return self.get_restart()

    def get_mod_time(self, tries_count):
        if tries_count > 30:
            log_print('Cannot find file, please make sure that the file is named exactly "{filename}"'.format(
                filename=self.passings_file_name))
            self.get_passings_export()
        else:
            try:
                result = os.path.getmtime(self.passings_file_name)
                return result
            except FileNotFoundError:
                if tries_count % 5 == 0:
                    log_print('Waiting for {filename} export...'.format(filename=self.passings_file_name))
                tries_count += 1
                time.sleep(2)
                return self.get_mod_time(tries_count)

    def get_passings_export(self):
        log_print("Please export {filename}".format(filename=self.passings_file_name))
        if abs(self.get_mod_time(0) - time.time()) < 3:
            log_print('Export Found!')
            time.sleep(1)
        else:
            log_print(
                "{filename} is too old. Deleting {filename}, wait for prompt to export".format(
                    filename=self.passings_file_name))
            os.remove(self.passings_file_name)
            self.get_passings_export()

    def start_monitors(self):
        log_print('Initiating Monitors')
        while True:
            start_driver_stint_check(self.driver_stint_dict)
            start_abnormal_lap_check(self.abnormal_lap_dict)


start_up = Startup()
