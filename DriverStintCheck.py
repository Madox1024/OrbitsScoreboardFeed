from util import calc_millisec, fix_time, stint_check
from xmlparser import get_stint_info
import time

refresh_rate = 1

def gen_pit_time_dict():
    stint_info = get_stint_info()
    pit_times = {}
    for team in stint_info:
        pit_times[team['car_number']]= calc_millisec(fix_time(team['total_time']))
    return pit_times


old_pit_time = gen_pit_time_dict()
while True:
    new_pit_time = gen_pit_time_dict()
    stint_info = get_stint_info()
    for team in stint_info:
        car_number = team['car_number']
        if team['last_time_line'] != "Start/Finish":
            old_pit_time[car_number] = new_pit_time[car_number]
        elif stint_check(old_pit_time[car_number], new_pit_time[car_number]):
            print('Car '+car_number+' needs to pit')
    time.sleep(refresh_rate)
