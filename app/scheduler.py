"""Threaded Process that stores the Barge Client in the database in a specified time interval"""


import threading
from time import sleep
from app.config import Config
from app.resources import Jeeves
from app.connection import DEBUGGER

def schedule():
    DEBUGGER.info(' * Starting Scheduler Thread')
    while True:
        Jeeves.get_clients()
        sleep(Config.SCHEDULER_DELAY_TIME)

SCHEDULER = threading.Thread(name='Scheduler', 
                             target=schedule, 
                             daemon=True
                             )