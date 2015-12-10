# a helpful timer class that can be used by the "with" statement
# taken from https://github.com/harvard-cs205/cs205-homework/blob/master/HW2/util/timer.py
import time
class Timer(object):
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start