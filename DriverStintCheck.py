import time

from util import calc_millisec, fix_time, time_stamp
from xmlparser import get_stint_info

refresh_rate = 5

class DriverStint:

    def __init__(self, car_num):
        self.car_num = car_num
        self.pit_time = calc_millisec(fix_time(get_stint_info()[car_num]['total_time']))
        self.last_time_line = get_stint_info()[car_num]['last_time_line']
        self.in_pit = True
        self.over_stint_triggered = False

    def over_stint(self):
        if not(self.over_stint_triggered):
            timestamp = fix_time(get_stint_info()[self.car_num]['total_time'])
            print('{carnum} is over their 2 hour driver stint at {time}'.format(carnum=self.car_num, time=timestamp))
            self.over_stint_triggered = True

    def refresh_pit(self, new_pit):
        self.pit_time = new_pit

    def pit_stop(self, new_time_line, new_pit):
        self.last_time_line = new_time_line
        self.refresh_pit(new_pit)
        self.in_pit = True
        self.over_stint_triggered = False
        print('Pit Stop: {carnum} at {time}'.format(carnum=self.car_num, time=time_stamp(new_pit)))

    def stint_check(self, new_time):
        if new_time - self.pit_time > 7200000: # MS in 2 hours
            return True
        else:
            return False

driver_stint_list = [DriverStint(team) for team in get_stint_info()]
while True:
    for driver in driver_stint_list:
        new_driver_info = get_stint_info()[driver.car_num]
        driver.last_time_line = new_driver_info['last_time_line']
        if driver.last_time_line == "Start/Finish":
            driver.in_pit = False
            if driver.stint_check(calc_millisec(fix_time(new_driver_info['total_time']))):
                driver.over_stint()
        elif driver.last_time_line != "Start/Finish" and driver.in_pit == False:
            driver.pit_stop(new_driver_info['last_time_line'], calc_millisec(fix_time(new_driver_info['total_time'])))
    time.sleep(refresh_rate)
