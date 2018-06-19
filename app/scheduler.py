"""Threaded Process that stores the Barge Client in the database in a specified time interval"""


import threading
from time import sleep

import app.resources
from app.config import Config
from app.connection import DEBUGGER

m, s = divmod(Config.SCHEDULER_DELAY_TIME, 60)
h, m = divmod(m, 60)
naptime = "%d hour, %d minutes, and %d seconds" % (h, m, s)

class Scheduler(object):
    isStarted = False

    def schedule():
        while True:
            DEBUGGER.info('Sleeping for {}.'.format(naptime))
            sleep(Config.SCHEDULER_DELAY_TIME)
            get_clients()

    SCHEDULER = threading.Thread(name='Scheduler', 
                             target=schedule, 
                             daemon=True
                             )    

    def safe_start(self):
        if(self.isStarted):
            DEBUGGER.debug('Scheduler already instantiated. Aborting start attempt.')
            return
        else:
            DEBUGGER.info('Starting Scheduler Thread')
            self.isStarted = True
            self.SCHEDULER.start()
