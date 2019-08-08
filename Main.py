import os

from Util import calc_millisec
from Parser import get_race_data, get_last_pit_lap, parse_lap_times

race_data = get_race_data()
last_pit_lap = get_last_pit_lap()
lap_times = parse_lap_times()


def lap_times_mod_time():
    result = os.path.getmtime('TestLapTimes.csv')
    return result


def get_old_pits():
    current_time = calc_millisec(race_data['timeofday']+'.000')
    race_time = calc_millisec(race_data['racetime']+'.000')
    race_time_diff = abs(current_time - race_time)

    last_pit_laps = {}
    for team in last_pit_lap:
        last_pit_laps[team] = last_pit_lap[team]['last_pit_lap']  # populating last_pit_laps w/ {car_num: lastpitlap #}

    team_last_pit_dict = {}
    for car in last_pit_laps:
        if car not in lap_times:
            team_last_pit_dict[car] = "0"  # LapTimes.csv drops cars w/ no passings, must avoid key error
        elif current_time >= race_time:
            last_pit_tod = calc_millisec(lap_times[car][last_pit_laps[car]])  # fetching respective lap times using
            team_last_pit_dict[car] = last_pit_tod - race_time_diff           # car number and selecting last pit time
        else:
            last_pit_tod = calc_millisec(lap_times[car][last_pit_laps[car]])  # this accounts for races that run past
            team_last_pit_dict[car] = last_pit_tod + race_time_diff           # 23:59:59 (TOD)
    return team_last_pit_dict
print(get_old_pits())