from static.utils.acManager import AcManager
from threading import Timer, Thread
from time import sleep
import datetime

class Scheduler(object):
    def __init__(self, sleep_time, function):
        self.sleep_time = sleep_time
        self.function = function
        self._t = None
        self._first = True

    def start(self):
        if self._t is None:
            if self._first:
                self._first = False
                self.function()
            self._t = Timer(self.sleep_time, self._run)
            self._t.start()
        else:
            raise Exception("this timer is already running")

    def _run(self):
        print(datetime.datetime.now())
        self.function()
        self._t = Timer(self.sleep_time, self._run)
        self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None

def test():
    print('test')


if __name__ == '__main__':
    from static.utils.acManager import AcManager
#    scheduler = Scheduler(86400, AcManager.run)
#    scheduler = Scheduler(86400, test)
#    scheduler.start()
    print('start crawel!')
    AcManager.run()   
    print('end')
