import time

from util import calc_millisec, fix_time, time_stamp
from xmlparser import get_stint_info

refresh_rate = 5


class DriverStint:
    # Overall this is a really awesome first stab at using objects. Plenty of room for improvement, but I'd never guess
    # this was your first time using objects if I didn't know better

    def __init__(self, car_num):
        self.car_num = car_num
        self.pit_time = calc_millisec(fix_time(get_stint_info()[car_num]['total_time']))
        self.last_time_line = get_stint_info()[car_num]['last_time_line']
        # VB A couple ways this could be improved

        # First, it's probably better to call get_stint_info() outside the constructor, and just pass in the specific
        # values you need. Generally the init/constructor should get all the parameters it needs from the calling class.
        # Doing stuff like file access (or other non-deterministic things) inside the constructor is a code smell

        # Second, since get_stint_info() is a pretty hefty function that's doing all that work to read and parse a file
        # each time you call it, so rather than calling it twice in  succession, call it once, put it in a variable,
        # and then read the results from that variable. Calling it twice in row like that also allows for a potential
        # bug if the file is updated between the first and second reads, and good luck tracking down a bug like that.
        # Try using right click -> refactor -> extract -> variable on get_stint_info()

        self.in_pit = True
        self.over_stint_triggered = False

    def over_stint(self):
        if not(self.over_stint_triggered):
            timestamp = fix_time(get_stint_info()[self.car_num]['total_time'])
            print('{carnum} is over their 2 hour driver stint at {time}'.format(carnum=self.car_num, time=timestamp))
            self.over_stint_triggered = True

    def refresh_pit(self, new_pit):
        self.pit_time = new_pit

    def pit_stop(self, new_time_line, new_pit):
        self.last_time_line = new_time_line
        self.refresh_pit(new_pit)
        self.in_pit = True
        self.over_stint_triggered = False
        print('Pit Stop: {carnum} at {time}'.format(carnum=self.car_num, time=time_stamp(new_pit)))

    def stint_check(self, new_time):
        if new_time - self.pit_time > 7200000:  # MS in 2 hours
            # VB Recommend rewrite as `2*60*60*1000`, much easier to visually parse, harder to drop a zero
            return True
        else:
            return False


driver_stint_list = [DriverStint(team) for team in get_stint_info()]
while True:
    for driver in driver_stint_list:
        new_driver_info = get_stint_info()[driver.car_num]
        driver.last_time_line = new_driver_info['last_time_line']
        # You call `calc_millisec(fix_time(new_driver_info['total_time']))` twice already,
        # 3 times if you make the changes I suggest. Definitely worth putting in a variable inside the loop for reuse
        if driver.last_time_line == "Start/Finish":
            driver.in_pit = False
            if driver.stint_check(calc_millisec(fix_time(new_driver_info['total_time']))):
                driver.over_stint()
                # As a way to move the print() call out of the object, you could change this to something like
                # if driver.stint_check(...) and not driver.over_stint_triggered
                #   driver.over_stint_triggered = true
                #   print("Over 2 hours etc")
                #

        elif driver.last_time_line != "Start/Finish" and driver.in_pit == False:
            # VB Nitpick, but you can remove the first half of this conditional,
            # since it's guaranteed to be true (i.e. not equal) given the previous branch
            driver.pit_stop(new_driver_info['last_time_line'], calc_millisec(fix_time(new_driver_info['total_time'])))
            # I suggest taking the print() call out of the pit_stop method and just manually printing here
    time.sleep(refresh_rate)
