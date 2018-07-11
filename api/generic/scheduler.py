"""Threaded Process that runs a function continuously separated a specified time interval"""

import os
import threading
import logging
from time import sleep

from .logger import time_execution

class Scheduler(object):
    """Thread to regularly run a background function"""

    hasRun = os.environ.get("WERKZEUG_RUN_MAIN")

    def __init__(self, func, interval=60):
        self.func = func
        self.interval = interval

        self.thread = threading.Thread(target=self.schedule)
        self.thread.name='Scheduler'
        self.thread.daemon=True  

    def safe_start(self):
        """Instantiates a Scheduler that will regularly run the given function"""
        if(self.hasRun):
            logging.debug('Scheduler already instantiated. Aborting start attempt.')
            return
        else:
            logging.info('Starting Scheduler Thread')
            self.thread.start()

    def schedule(self):
        """Waits, then runs function"""
        while True:
            self.wait(self.interval)
            self.do_job()

    @time_execution
    def do_job(self):
        self.func()
            
    def wait(self, interval):
        """Sleeps the thread for the interval of time given

        Arguments:
            interval {int} -- interval (in seconds) to sleep the thread"""
        m, s = divmod(interval, 60)
        h, m = divmod(m, 60)
        naptime = "%dh, %dm, %ds" % (h, m, s)
        logging.debug('Sleeping for {}.'.format(naptime))
        sleep(interval)