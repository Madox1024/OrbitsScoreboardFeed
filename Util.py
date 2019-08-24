

def calc_millisec(time_stamp):
    try:
        time_stamp_ms = fix_time(time_stamp)
        millisec = int(time_stamp_ms[-3:])
        seconds = int(time_stamp_ms[-6:-4]) * 1000
        minutes = int(time_stamp_ms[-9:-7]) * (60 * 1000)
        hours = int(time_stamp_ms[-12:-10]) * ((60 * 1000) * 60)
        total_ms = millisec + seconds + minutes + hours
        return total_ms
    except ValueError:
        print('Value Error: "{timestamp}"'.format(timestamp=time_stamp))
        return time_stamp


def gen_time_stamp(milliseconds):
    millisecond_str = str(milliseconds)
    total_seconds = milliseconds/1000

    millisec = millisecond_str[-3:]
    second = int(total_seconds % 60)
    minute = int((total_seconds/60) % 60)
    hour = int((total_seconds/60)/60)
    return '{hour}:{minute}:{second}.{millisec}'.format(hour=hour, minute=minute, second=second, millisec=millisec)


def fix_time(t):
    default = '00:00:00.000'
    if t == '':
        result = default
    else:
        if t[-4] != '.':
            t = t + '.000'
        if len(t) < 12:
            result = default[:12 - len(t)] + t
        else:
            result = t
    return result
