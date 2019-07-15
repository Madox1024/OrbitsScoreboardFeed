import time
from xmlparser import get_stint_info


def fix_time(t):
    ft = t[:-4]
    if len(t) < 11:
        ft = '00:'+ft
    return str('2010;'+ft) #must add year to avoid Overflow Error


def gen_pit_time_lst():
    stint_info = get_stint_info()
    pit_times = []
    for team in stint_info:
        #if team['last_time_line'] != 'Start/Finish': >>>> Possibly move this logic to stint checker
        pit_time = {
            'car_number': team['car_number'],
            'pit_time': time.mktime(time.strptime(fix_time(team['total_time']), '%Y;%H:%M:%S'))
        }
        pit_times.append(pit_time)
    return pit_times
print(gen_pit_time_lst())

def stint_check(old_pit, new_pit):
    if new_pit - old_pit > 7200 # sec in 2 hours
        return True
    else:
        return False

#need to add logic to refresh pit times @ pit stops AND constantly stint_check()