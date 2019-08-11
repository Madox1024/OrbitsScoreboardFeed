import time

from Parser import get_last_pit_dict, get_stint_info
from Util import calc_millisec, fix_time, gen_time_stamp

refresh_rate = 1


class DriverStint:

    def __init__(self, reg_num, init_stint_info):
        self.reg_num = reg_num
        self.initial_stint_info = init_stint_info
        self.car_num = self.initial_stint_info[reg_num]['car_number']
        self.pit_time = calc_millisec(self.initial_stint_info[reg_num]['total_time'])
        self.last_time_line = self.initial_stint_info[reg_num]['last_time_line']
        self.in_pit = True
        self.over_stint_triggered = False

    def over_stint(self):
        if not self.over_stint_triggered:
            self.over_stint_triggered = True

    def refresh_pit(self, new_pit):
        self.pit_time = new_pit

    def pit_stop(self, new_time_line, new_pit):
        self.last_time_line = new_time_line
        self.refresh_pit(new_pit)
        self.in_pit = True
        self.over_stint_triggered = False

    def stint_check(self, new_time):
        if new_time - int(self.pit_time) > 2*60*60*1000:  # milliseconds in 2 hours
            #  self.pit_time is converted to an integer in calc_millisec()
            #  but getting Error: cannot subtract int and str, quick fix: int(self.pit_time)
            return True
        else:
            return False


def missing_driver(car_num):
    print('Car {carnum} is missing from the scoreboard feed and is no longer being monitored!'.format(carnum=car_num))


def add_driver(driver_dict, stint_info):
    for driver in stint_info:
        if driver not in driver_dict:
            new_driver_obj = DriverStint(driver, stint_info)
            return new_driver_obj


def instantiate_driver_stint():
    got_stint_info = get_stint_info()
    driver_stint_dict = {}
    for team in got_stint_info:
        driver_stint_dict[team] = DriverStint(team, got_stint_info)
    return driver_stint_dict


def instantiate_with_old_pit_times():
    driver_stint_dict = instantiate_driver_stint()
    last_pit_dict = get_last_pit_dict()
    for driver_key in driver_stint_dict:
        driver = driver_stint_dict[driver_key]
        if driver.car_num in last_pit_dict:
            driver.refresh_pit(last_pit_dict[driver.car_num])
    return driver_stint_dict


def start_driver_stint_check(restart):
    if restart:
        driver_stint_dict = instantiate_with_old_pit_times()
    else:
        driver_stint_dict = instantiate_driver_stint()

    while True:

        stint_info = get_stint_info()
        if len(driver_stint_dict) < len(stint_info):
            new_driver = add_driver(driver_stint_dict, stint_info)
            driver_stint_dict[new_driver.reg_num] = new_driver
            print('Car {carnum} successfully added and is being monitored'.format(carnum=new_driver.car_num))

        for driver_key in driver_stint_dict:
            driver = driver_stint_dict[driver_key]
            if driver.reg_num not in stint_info:
                missing_driver(driver.car_num)
                break

            new_driver_info = stint_info[driver.reg_num]
            driver.last_time_line = new_driver_info['last_time_line']
            new_lap_time = calc_millisec(new_driver_info['total_time'])

            if driver.last_time_line == "Start/Finish":
                driver.in_pit = False
                if driver.stint_check(new_lap_time) and not driver.over_stint_triggered:
                    driver.over_stint()
                    current_time_stamp = fix_time(stint_info[driver.reg_num]['total_time'])
                    print('{carnum} is over their 2 hour driver stint at {time}'.format(carnum=driver.car_num,
                                                                                        time=current_time_stamp))

            elif not driver.in_pit:
                driver.pit_stop(new_driver_info['last_time_line'], new_lap_time)
                print('Pit Stop: {carnum} at {time}'.format(carnum=driver.car_num, time=gen_time_stamp(new_lap_time)))
        time.sleep(refresh_rate)
