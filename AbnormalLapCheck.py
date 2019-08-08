from Util import calc_millisec
from Parser import get_leader_board, get_race_data

# WIP

refreshrate = 1


class TeamLapCheck:

    def __init__(self, car_num, init_leader_board, init_race_data):
        self.car_num = car_num
        self.initial_race_data = init_race_data
        self.initial_leader_board = init_leader_board
        self.avg_lap_time = self.initial_leader_board[car_num]['avg_lap_time']
        self.since_pit = self.initial_leader_board[car_num]['since_pit']
        self.last_time = self.initial_leader_board[car_num]['last_time']
        self.total_time = self.initial_leader_board[car_num]['total_time']
        self.race_time = self.initial_race_data['racetime']
        self.drop_out_triggered = False

    def refresh_info(self):
        leader_board = get_leader_board()
        self.avg_lap_time = leader_board[self.car_num]['avg_lap_time']
        self.since_pit = leader_board[self.car_num]['since_pit']
        self.last_time = leader_board[self.car_num]['last_time']
        self.total_time = leader_board[self.car_num]['total_time']
        self.race_time = get_race_data()['racetime']

    def long_lap(self):
        pass

    def over_double_lap(self):
        pass

    def drop_out(self):
        pass

    def drop_out_check(self):
        race_time = calc_millisec(self.race_time)
        total_time = calc_millisec(self.total_time)
        if race_time - total_time > 600000:  # 10 min
            return True
        else:
            return False

    def check_time(self, last_time):
        self.refresh_info()
        avg_time_ms = calc_millisec(self.avg_lap_time)
        is_1min_over = avg_time_ms <= (last_time - 60000)
        is_over_double = avg_time_ms * 2 <= last_time
        if is_1min_over and not is_over_double:  # 1 min
            self.long_lap()
        elif is_over_double:
            self.over_double_lap()
        elif self.drop_out_check() and not self.drop_out_triggered:
            self.drop_out()
