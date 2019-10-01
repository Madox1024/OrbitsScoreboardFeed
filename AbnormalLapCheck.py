import time

from Util import calc_millisec, log_print

refresh_rate = .5


class TeamLapCheck:

    def __init__(self, reg_num, init_leader_board, init_race_data):
        self.reg_num = reg_num
        self.car_num = init_leader_board[reg_num]['car_num']
        self.best_lap_time = init_leader_board[reg_num]['best_lap_time']
        self.last_time = init_leader_board[reg_num]['last_time']
        self.total_time = init_leader_board[reg_num]['total_time']
        self.race_time = init_race_data['racetime']
        self.flag = init_race_data['flag']
        self.laps_since_pit = int(init_leader_board[reg_num]['since_pit'])
        self.msg_triggered = False
        self.drop_out_triggered = False

    def refresh_info(self, xml_parser):
        leader_board = xml_parser.get_leader_board()
        race_data = xml_parser.get_race_data()
        self.car_num = leader_board[self.reg_num]['car_num']
        self.best_lap_time = leader_board[self.reg_num]['best_lap_time']
        self.last_time = leader_board[self.reg_num]['last_time']
        self.total_time = leader_board[self.reg_num]['total_time']
        self.race_time = race_data['racetime']
        self.flag = race_data['flag']
        self.laps_since_pit = int(leader_board[self.reg_num]['since_pit'])

    def message_trigger(self):
        self.msg_triggered = True

    def drop_out(self):
        self.drop_out_triggered = True
        self.msg_triggered = True

    def normal_lap(self):
        self.msg_triggered = False
        self.drop_out_triggered = False

    def drop_out_check(self):
        race_time = calc_millisec(self.race_time)
        total_time = calc_millisec(self.total_time)
        if race_time - total_time > 20 * 60 * 1000:  # 20 min
            return True
        else:
            return False

    def normal_lap_check(self):
        if self.last_time != 'IN PIT' and self.last_time != '':
            abs_lap_diff = abs(calc_millisec(self.last_time) - calc_millisec(self.best_lap_time))
            if abs_lap_diff < 30 * 1000 and (not self.drop_out_triggered):
                return True
            else:
                return False
        else:
            return True  # if last time is not a times stamp then it is considered a normal lap

    def check_time(self, last_time, xml_parser):

        self.flag = xml_parser.get_race_data()['flag']  # refresh to current flag status
        not_triggered = (not self.msg_triggered) and (not self.drop_out_triggered)

        if self.flag == 'green':  # ignore abnormal laps when not green

            self.refresh_info(xml_parser)
            not_out_lap = self.laps_since_pit > 1  # only checks laps after pit out lap

            if not_out_lap:

                best_time_ms = calc_millisec(self.best_lap_time)

                abnormal_short = best_time_ms + (60*1000) <= last_time < (best_time_ms * 2)
                over_double = (best_time_ms * 2) <= last_time < (best_time_ms * 2) + (30*1000)
                abnormal_long = (best_time_ms * 2) + (30*1000) <= last_time < (20*60*1000) - last_time

                if abnormal_short and not_triggered:
                    self.message_trigger()
                    log_print('Car {carnum} is 1 min over their avg laptime at {time}'.format(carnum=self.car_num,
                                                                                              time=self.total_time))

                elif over_double and not_triggered:
                    self.message_trigger()
                    log_print('Car {carnum} has a lap twice their avg at {time}'.format(carnum=self.car_num,
                                                                                        time=self.total_time))

                elif abnormal_long and not_triggered:
                    self.message_trigger()
                    log_print('Car {carnum} has an abnormally long lap at: {time}'.format(carnum=self.car_num,
                                                                                          time=self.total_time))
                elif self.normal_lap_check():
                    self.normal_lap()
        if self.drop_out_check() and not_triggered:
            self.drop_out()
            log_print(
                'Car {carnum} has not hit for 20 mins, last crossing at {time}'.format(carnum=self.car_num,
                                                                                       time=self.total_time))


def instantiate_team_lap_check(xml_parser):
    leader_board = xml_parser.get_leader_board()
    race_data = xml_parser.get_race_data()
    team_obj_dict = {}
    for team in leader_board:
        team_obj_dict[team] = TeamLapCheck(team, leader_board, race_data)
    return team_obj_dict


def add_driver(driver_dict, leader_board, xml_parser):
    for team in leader_board:
        if team not in driver_dict:
            new_team_obj = TeamLapCheck(team, xml_parser.get_leader_board(), xml_parser.get_race_data())
            return new_team_obj


def abnormal_lap_check(team_obj_dict, xml_parser):
    leader_board = xml_parser.get_leader_board()
    if len(team_obj_dict) < len(leader_board):
        new_driver = add_driver(team_obj_dict, leader_board, xml_parser)
        team_obj_dict[new_driver.reg_num] = new_driver
        log_print('{carnum} added to Lap-Checker'.format(carnum=team_obj_dict[new_driver.car_num]))

    for driver_key in team_obj_dict:
        driver = team_obj_dict[driver_key]
        if driver.reg_num not in leader_board:
            instantiate_team_lap_check(xml_parser)
            log_print('Reinstantiating TeamLapCheck')
            break
        driver_last_time = leader_board[driver.reg_num]['last_time']
        if (driver_last_time != '') and (driver_last_time != 'IN PIT'):
            new_lap_time = calc_millisec(driver_last_time)
            driver.check_time(new_lap_time, xml_parser)
    time.sleep(refresh_rate)
