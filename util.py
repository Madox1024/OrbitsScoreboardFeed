

def calc_milisec(time_stamp):
    milisec = int(time_stamp[-3:])
    seconds = int(time_stamp[-6:-4]) * 1000
    minutes = int(time_stamp[-9:-7]) * (60 * 1000)
    hours = int(time_stamp[-12:-10]) * ((60*1000)*60)
    total_ms = milisec + seconds + minutes + hours
    return total_ms