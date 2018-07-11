import logging
import time

import api
from .config import Config
from .models import Client, RequestLog, LogAndClient

class Util():
    """Functions to work with the CMX framework"""

    @staticmethod
    def url_from(start, step):
            """Forms proper url from start and step given, then makes CMX API call

            Returns:
                (flag, _clients) {tuple} -- flag: if it was a valid iterate, _clients: list of clients"""
            # Define the RangeEnd by the RangeStart and RangeStep
            end = start + step
            # Form the url out of the new RangeStart and RangeEnd
            _arguments = "?locatedAfterTime={}&locatedBeforeTime={}".format(start, end)
            _url = Config.WEB['URL']+_arguments
            return _url 

    class step():
        """Functions pertaining to a request step"""

        @staticmethod
        def restrict_time_travel(start, step):
            """Makes sure the step won't go into the future
            
            Arguments:
                start {int} -- time to start from
                step {int} -- increment to step by
            
            Returns:
                int -- valid step distance to not cause unintentional time travel
            """
            # Create a step value from the current time
            _now = int(round(time.time()) * 1000)
            _step_from_now = _now - start

            # Return the minimum of these steps. Essentially: "if timeTravel: don't!"
            return min(step, _step_from_now) 

        @staticmethod
        def refactor(refactor_func, step):
            """Resizes the step size based on the refactor_function
            
            Arguments:
                refactor_func {func} -- function to resize the step
                step {int} -- step size in millis
            
            Returns:
                int -- resized step
            """

            logging.warning('Client count exceeds max. Retrying call with half-sized step.')
            _new_step = refactor_func(step)
            return _new_step

        @staticmethod
        def half(step):
            return step//2

        @staticmethod
        def cieldiv(a, b):
            return -(-a // b)  

class StepIterator():
    """The machine that collects all the data from the CMX server
    
    Arguments:
        baseStep {int} -- the base time increment to step when making a CMX call
    """

    def __init__(self, baseStep):
        self.base_step = baseStep
        self.last_log = RequestLog.most_recent() 

    def iterate_by(self, step):
        """Obtains Clients from given start, step range
        
        Arguments:
            step {int} -- time to step by
        
        Returns:
            tuple -- (new request log, all pulled clients)
        """

        # Get the RangeEnd of the last RequestLog. If there's no RequestLogs, return the defined start time from the config
        _start = Config.API['RANGE_START'] if self.last_log.RangeEnd is None else self.last_log.RangeEnd
        # Determines if the step given goes into the future and if so, returns a valid step to now
        _step = Util.step.restrict_time_travel(_start, step)
        # Create URL from interval
        _url = Util.url_from(_start, _step)
        # Obtain the data from the CMX call as defined by the _url
        _client_data = api.conn.get_json_from(_url)    
        # The ammount of clients in the collected data
        _client_count = len(_client_data)
        # If the count was 5K, initiate half-step recursive call
        if _client_count == 5000:
            _new_step = Util.step.refactor(Util.step.half, _step)
            return self.iterate_by(_new_step)
        # Turn the client data returned from the successful call into the ORM client list
        _clients = Client.group.from_data(_client_data)
        # Create a new RequestLog with data
        _new_log = RequestLog.from_step(_start, _step, _client_count)
        # Update the last log to be the new one. Any math done on last quantity would be done before this.
        self.last_log = _new_log
        # Store everything to database
        _new_log, _clients = LogAndClient.to_database(_new_log, _clients)

        return (_new_log, _clients)
  
    def base_iterate(self):
        """Pull data from next base-range interval"""
        return self.iterate_by(self.base_step)
