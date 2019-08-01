import time

from Util import calc_millisec, fix_time, gen_time_stamp
from XMLParser import get_stint_info

refresh_rate = 5


class DriverStint:

    def __init__(self, car_num, init_stint_info):
        self.car_num = car_num
        self.initial_stint_info = init_stint_info
        self.pit_time = calc_millisec(self.initial_stint_info[car_num]['total_time'])
        self.last_time_line = self.initial_stint_info[car_num]['last_time_line']
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


def instantiate_driver_stint():
    global driver_stint_list
    got_stint_info = get_stint_info()
    driver_stint_list = [DriverStint(team, got_stint_info) for team in got_stint_info]


def start_driver_stint_check():
    instantiate_driver_stint()
    while True:

        stint_info = get_stint_info()
        if len(driver_stint_list) != len(stint_info):
            instantiate_driver_stint()

        for driver in driver_stint_list:
            if driver.car_num not in stint_info:
                instantiate_driver_stint()
                break
                #  figure out a way to pass changed car num info?

            new_driver_info = stint_info[driver.car_num]
            driver.last_time_line = new_driver_info['last_time_line']
            new_lap_time = calc_millisec(new_driver_info['total_time'])

            if driver.last_time_line == "Start/Finish":
                driver.in_pit = False
                if driver.stint_check(new_lap_time) and not driver.over_stint_triggered:
                    driver.over_stint()
                    current_time_stamp = fix_time(stint_info[driver.car_num]['total_time'])
                    print('{carnum} is over their 2 hour driver stint at {time}'.format(carnum=driver.car_num,
                                                                                        time=current_time_stamp))

            elif not driver.in_pit:
                driver.pit_stop(new_driver_info['last_time_line'], new_lap_time)
                print('Pit Stop: {carnum} at {time}'.format(carnum=driver.car_num, time=gen_time_stamp(new_lap_time)))
        time.sleep(refresh_rate)
