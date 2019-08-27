import time

from Parser import get_leader_board, get_race_data
from Util import calc_millisec, log

# WIP

refreshrate = 1


class TeamLapCheck:

    def __init__(self, reg_num, init_leader_board, init_race_data):
        self.reg_num = reg_num
        self.initial_race_data = init_race_data
        self.initial_leader_board = init_leader_board
        self.car_num = self.initial_leader_board[reg_num]['car_num']
        self.best_lap_time = self.initial_leader_board[reg_num]['best_lap_time']
        self.last_time = self.initial_leader_board[reg_num]['last_time']
        self.total_time = self.initial_leader_board[reg_num]['total_time']
        self.race_time = self.initial_race_data['racetime']
        self.flag = self.initial_race_data['flag']
        self.laps_since_pit = int(self.initial_leader_board[reg_num]['since_pit'])
        self.msg_triggered = False
        self.drop_out_triggered = False

    def refresh_info(self):
        leader_board = get_leader_board()
        self.car_num = leader_board[self.reg_num]['car_num']
        self.best_lap_time = leader_board[self.reg_num]['best_lap_time']
        self.last_time = leader_board[self.reg_num]['last_time']
        self.total_time = leader_board[self.reg_num]['total_time']
        self.race_time = get_race_data()['racetime']

    def long_lap(self):
        self.msg_triggered = True

    def over_double_lap(self):
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
        if race_time - total_time > 20 * 60 * 1000:  # 10 min
            return True
        else:
            return False

    def normal_lap_check(self):
        if self.last_time != 'IN PIT' and self.last_time != '':
            abs_lap_diff = abs(calc_millisec(self.last_time) - calc_millisec(self.best_lap_time))
        else:
            log('Car {carnum} \n  Resetting lap state'.format(carnum=self.car_num))
            abs_lap_diff = 0
        if abs_lap_diff < 30 * 1000 and (not self.drop_out_triggered):
            # will not reset after drop_out, figure out a way to reset after dropout
            return True
        else:
            return False

    def check_time(self, last_time):
        self.refresh_info()
        if (self.flag != 'yellow') and (last_time != 'IN PIT'):
            if self.laps_since_pit != 1:

                best_time_ms = calc_millisec(self.best_lap_time)
                is_1min_over = best_time_ms <= (last_time - (60 * 1000))
                is_over_double = (best_time_ms * 2) <= last_time < (best_time_ms * 3)
                not_triggered = (not self.msg_triggered) and (not self.drop_out_triggered)

                if is_1min_over and (not is_over_double) and not_triggered:
                    self.long_lap()
                    log('Car {carnum} has a long lap at {time}'.format(carnum=self.car_num, time=self.total_time))

                elif is_over_double and not_triggered:
                    self.over_double_lap()
                    log('Car {carnum} might have missed a lap at {time}'.format(carnum=self.car_num,
                                                                                time=self.total_time))

                elif self.drop_out_check() and not_triggered:
                    self.drop_out()
                    log('Car {carnum} is not hitting, last crossing at {time}'.format(carnum=self.car_num,
                                                                                      time=self.total_time))
                elif self.normal_lap_check():
                    self.normal_lap()
            elif not self.msg_triggered:
                log('Cannot resolve {carnum} last lap time: "{lasttime}"'.format(carnum=self.car_num,
                                                                                 lasttime=last_time))
                self.msg_triggered = True


def instantiate_team_lap_check():
    leader_board = get_leader_board()
    race_data = get_race_data()
    team_obj_dict = {}
    for team in leader_board:
        team_obj_dict[team] = TeamLapCheck(team, leader_board, race_data)
    return team_obj_dict


def add_driver(driver_dict, leader_board):
    for team in leader_board:
        if team not in driver_dict:
            new_team_obj = TeamLapCheck(team, get_leader_board(), get_race_data())
            return new_team_obj


def start_abnormal_lap_check(team_obj_dict):
    leader_board = get_leader_board()
    if len(team_obj_dict) < len(leader_board):
        new_driver = add_driver(team_obj_dict, leader_board)
        team_obj_dict[new_driver.reg_num] = new_driver
        log('Add driver triggered')

    for driver_key in team_obj_dict:
        driver = team_obj_dict[driver_key]
        if driver.reg_num not in leader_board:
            instantiate_team_lap_check()
            log('Reinstantiating TeamLapCheck')
            break
        if leader_board[driver.reg_num]['last_time'] != '':
            new_lap_time = calc_millisec(leader_board[driver.reg_num]['last_time'])
            driver.check_time(new_lap_time)
    time.sleep(refreshrate)
