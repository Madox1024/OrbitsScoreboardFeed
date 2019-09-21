import time


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
        log_print('Value Error - calc_millisec({timestamp})'.format(timestamp=time_stamp))
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


def log_print(message):
    time_stamp = (time.ctime(time.time()))
    file_name = time_stamp[:-13] + ' Log File.txt'
    with open(file_name, 'a+') as log_file:
        log_message = message + ' ' + time_stamp[11:]
        log_file.write(log_message + '\n')
        print(message)


def log_only(message):
    time_stamp = (time.ctime(time.time()))
    file_name = time_stamp[:-13] + ' Log File.txt'
    with open(file_name, 'a+') as log_file:
        fixed_stamp = message + ' ' + time_stamp[11:]
        log_file.write(fixed_stamp + '\n')
