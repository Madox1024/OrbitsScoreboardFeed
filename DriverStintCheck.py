import time

from Util import calc_millisec, fix_time, gen_time_stamp, log_print, log_only

refresh_rate = .5


class DriverStint:

    def __init__(self, reg_num, init_stint_info):
        self.reg_num = reg_num
        self.initial_stint_info = init_stint_info
        self.car_num = self.initial_stint_info[reg_num]['car_number']
        self.pit_time = calc_millisec(self.initial_stint_info[reg_num]['total_time'])
        self.last_time_line = self.initial_stint_info[reg_num]['last_time_line']
        self.pit_msg_sent = False
        self.over_stint_triggered = False

    def over_stint(self):
        if not self.over_stint_triggered:
            self.over_stint_triggered = True

    def refresh_pit(self, new_pit):
        self.pit_time = new_pit

    def pit_stop(self, new_time_line, new_pit):
        self.last_time_line = new_time_line
        self.refresh_pit(new_pit)
        self.over_stint_triggered = False

    def stint_check(self, new_time):
        if new_time - int(self.pit_time) > 2*60*60*1000:  # milliseconds in 2 hours
            #  self.pit_time should be converted to an integer in calc_millisec()
            #  but getting Error: cannot subtract int and str, -> quick fix: int(self.pit_time)
            return True
        else:
            return False


def add_driver(driver_dict, stint_info):
    for driver in stint_info:
        if driver not in driver_dict:
            new_driver_obj = DriverStint(driver, stint_info)
            return new_driver_obj


def instantiate_driver_stint(get_stint_info):
    stint_info = get_stint_info
    driver_stint_dict = {}
    for team in stint_info:
        driver_stint_dict[team] = DriverStint(team, stint_info)
    return driver_stint_dict


def instantiate_with_old_pit_times(gen_last_pit_dict, get_stint_info):
    driver_stint_dict = instantiate_driver_stint(get_stint_info)
    last_pit_dict = gen_last_pit_dict
    for driver_key in driver_stint_dict:
        driver = driver_stint_dict[driver_key]
        if driver.car_num in last_pit_dict:
            old_pit_time = last_pit_dict[driver.car_num]
            driver.refresh_pit(old_pit_time)
            log_only('{carnum} imported pit stop at: {timestamp}'.format(carnum=driver.car_num,
                                                                         timestamp=gen_time_stamp(old_pit_time)))
        else:
            driver.refresh_pit(0)
            log_only('{carnum} no pit time, set to 0 ms'.format(carnum=driver.car_num))
    return driver_stint_dict


def start_dsc_instantiation(restart, gen_last_pit_dict, get_stint_info):
    if restart:
        result = instantiate_with_old_pit_times(gen_last_pit_dict, get_stint_info)
    else:
        result = instantiate_driver_stint(get_stint_info)
    return result


def start_driver_stint_check(driver_stint_dict, xml_parser):
    stint_info = xml_parser.new_stint_info()
    if len(driver_stint_dict) < len(stint_info):
        new_driver = add_driver(driver_stint_dict, stint_info)
        driver_stint_dict[new_driver.reg_num] = new_driver
        log_print('{carnum} added to Stint-Checker'.format(carnum=new_driver.car_num))

    for driver_key in driver_stint_dict:
        driver = driver_stint_dict[driver_key]
        if driver.reg_num not in stint_info:
            log_print(
                'Car {carnum} is missing from the scoreboard feed and is no longer being monitored!'.format(
                    carnum=driver.car_num)
            )
            driver_stint_dict.pop(driver_key)  # this needs testing
            break

        new_driver_info = stint_info[driver.reg_num]
        driver.last_time_line = new_driver_info['last_time_line']
        new_lap_time = calc_millisec(new_driver_info['total_time'])

        if driver.last_time_line == "Start/Finish":
            driver.pit_msg_sent = False
            if driver.stint_check(new_lap_time) and not driver.over_stint_triggered:
                driver.over_stint()
                current_time_stamp = fix_time(stint_info[driver.reg_num]['total_time'])
                log_print('{carnum} is nearing their 2 hour driver stint at {time}'.format(carnum=driver.car_num,
                                                                                           time=current_time_stamp))

        else:
            driver.pit_stop(new_driver_info['last_time_line'], new_lap_time)
            if not driver.pit_msg_sent:
                log_only('Pit Stop: {carnum} at {time}'.format(carnum=driver.car_num,
                                                               time=new_driver_info['total_time']))
                driver.pit_msg_sent = True
    time.sleep(refresh_rate)
