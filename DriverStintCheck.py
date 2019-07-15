from xmlparser import get_stint_info


def fix_time(t):
    if len(t) < 11:
        ft = '00:'+t
    else:
        ft = t
    return str(ft) #must add year to avoid Overflow Error


def calc_milisec(time_stamp):
    milisec = int(time_stamp[-3:])
    seconds = int(time_stamp[-6:-4]) * 1000
    minutes = int(time_stamp[-9:-7]) * (60 * 1000)
    hours = int(time_stamp[-12:-10]) * ((60*1000)*60)
    total_ms = milisec + seconds + minutes + hours
    return total_ms


def gen_pit_time_list():
    stint_info = get_stint_info()
    pit_times = []
    for team in stint_info:
        #if team['last_time_line'] != 'Start/Finish': >>>> Possibly move this logic to stint checker
        pit_time = {
            'car_number': team['car_number'],
            'pit_time': calc_milisec(fix_time(team['total_time']))
        }
        pit_times.append(pit_time)
    return pit_times
print(gen_pit_time_list())

def stint_check(old_pit, new_pit):
    if new_pit - old_pit > 7200: # sec in 2 hours
        return True
    else:
        return False

#need to add logic to refresh pit times @ pit stops AND constantly stint_check()