import time

from Parser import get_race_data, get_stint_info, get_last_pit_lap, parse_lap_times
from Util import calc_millisec, fix_time, gen_time_stamp

refresh_rate = 5


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
        if new_time - self.pit_time > 2*60*60*1000:  # milliseconds in 2 hours
            return True
        else:
            return False


race_data = get_race_data()
last_pit_lap = get_last_pit_lap()
lap_times = parse_lap_times()


def get_old_pits():
    current_time = calc_millisec(race_data['timeofday'])  # must add '.000' b/c race_data doesn't include ms
    race_time = calc_millisec(race_data['racetime'])
    race_time_diff = abs(current_time - race_time)

    last_pit_laps = {}
    for team in last_pit_lap:
        last_pit_laps[team] = last_pit_lap[team]['last_pit_lap']  # populating last_pit_laps w/ {car_num: lastpitlap #}

    team_last_pit_dict = {}
    for car in last_pit_laps:
        if car not in lap_times:
            team_last_pit_dict[car] = "0"  # LapTimes.csv drops cars w/ no passings, must avoid key error

        elif current_time >= race_time:
            last_pit_tod = calc_millisec(lap_times[car][last_pit_laps[car]])  # fetching respective lap times
            team_last_pit_dict[car] = last_pit_tod - race_time_diff           # using car number and selecting last pit

        else:
            last_pit_tod = calc_millisec(lap_times[car][last_pit_laps[car]])  # this accounts for races that
            team_last_pit_dict[car] = last_pit_tod + race_time_diff                  # run past 23:59:59 (TOD)

    return team_last_pit_dict


def missing_driver(car_num):
    print('Car {carnum} is missing from the scoreboard feed and is no longer being monitored!'.format(carnum=car_num))


def add_driver(driver_dict, stint_info):
    for driver in stint_info:
        if driver not in driver_dict:
            new_driver_stint = DriverStint(driver, stint_info)
            return new_driver_stint


def instantiate_driver_stint():
    got_stint_info = get_stint_info()
    driver_stint_dict = {}
    for team in got_stint_info:
        driver_stint_dict[team]: DriverStint(team, got_stint_info)
    return driver_stint_dict


def start_driver_stint_check():
    driver_stint_dict = instantiate_driver_stint()
    while True:

        stint_info = get_stint_info()
        if len(driver_stint_dict) < len(stint_info):
            new_driver = add_driver(driver_stint_dict, stint_info)
            driver_stint_dict[new_driver.reg_num] = new_driver
            print('Car {carnum} successfully added and is being monitored')

        for driver in driver_stint_dict:
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
