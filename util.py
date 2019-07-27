

def calc_millisec(time_stamp):
    millisec = int(time_stamp[-3:])
    seconds = int(time_stamp[-6:-4]) * 1000
    minutes = int(time_stamp[-9:-7]) * (60 * 1000)
    hours = int(time_stamp[-12:-10]) * ((60*1000)*60)
    total_ms = millisec + seconds + minutes + hours
    return total_ms

def time_stamp(milliseconds):
    millisecond_str = str(milliseconds)
    total_seconds = milliseconds/1000

    millisec = millisecond_str[-3:]
    second = int(total_seconds%60)
    minute = int((total_seconds/60)%60)
    hour = int((total_seconds/60)/60)
    return '{hour}:{minute}:{second}.{millisec}'.format(hour=hour, minute=minute, second=second, millisec=millisec)

def fix_time(t):
    if len(t) < 11:
        ft = '00:' + t
    else:
        ft = t
    return str(ft)

