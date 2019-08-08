import os

from XMLParser import get_race_data, get_stint_info, parse_lap_times
from Util import calc_millisec


race_data = get_race_data()
stint_info = get_stint_info()
lap_times = parse_lap_times()


def lap_times_mod_time():
    result = os.path.getmtime('TestLapTimes.csv')
    return result


def get_old_pits():
    current_time = calc_millisec(race_data['timeofday']+'.000')
    race_time = calc_millisec(race_data['racetime']+'.000')
    race_start_time = abs(current_time - race_time)

    last_pit_laps = {}
    for team in stint_info:
        last_pit_laps[team] = stint_info[team]['last_pit_lap']

    team_last_pit_dict = {}
    for car in last_pit_laps:
        if car not in lap_times:
            team_last_pit_dict[car] = "0"
        elif current_time >= race_time:
            last_pit_tod = calc_millisec(lap_times[car][last_pit_laps[car]])
            team_last_pit_dict[car] = last_pit_tod - race_start_time
        else:
            last_pit_tod = calc_millisec(lap_times[car][last_pit_laps[car]])
            team_last_pit_dict[car] = last_pit_tod + race_start_time
    return team_last_pit_dict
