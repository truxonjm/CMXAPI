"""Provides a safe and descriptive wrapper around requests to handle disconnects and error handling."""


import logging
from base64 import b64encode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .logger import time_execution

class SafeRequest():
    """Wrapper class around a requests session that integrates error handling and effective retries.

        Arguments:
            uid {str} -- Username for SSL Login
            pwd {str} -- Password for SSL Login
            verify {bool, or str} --  
                'False': Unsecured connection 
                'path to certification files': safe connection.
        
        Keyword Arguments:
            max_retries {int} -- Number of retries on failed connection type defined by status_forcelist (default: {3})
            backoff_factor {float} -- {backoff factor} * (2 ^ ({number of total retries} - 1)) (default: {.5})
            status_forcelist {[type]} -- List of status codes to retry connection on (default: [500,503,504])"""

    def __init__(self, uid, pwd, verify, max_retries=3, backoff_factor=.5, status_forcelist=None):
        _upStr = "{}:{}".format(uid,pwd)
        self.auth = b64encode(_upStr.encode()).decode("ascii")
        self.headers = {
            'Authorization' : 'Basic %s' % self.auth,
            'Cache-Control': "no-cache",
            'Postman-Token': "e4cca5bc-11fb-493f-a169-c82d31b78c5b"
            }
        self.verify = verify
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.status_forcelist =  status_forcelist or [500,503,504]

    def requests_retry_session(self, session=None):
        """Wrapper around session that handles retries.
        
        Keyword Arguments:
            session {Requests session} -- (default: {None})
        
        Returns:
            Requests session 
        """
        _session = session or requests.Session()
        
        _retry = Retry(
            total=self.max_retries,
            read=self.max_retries,
            connect=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        _adapter = HTTPAdapter(max_retries=_retry)
        _session.mount('http://', _adapter)
        _session.mount('https://', _adapter)
        return _session

    @time_execution
    def get_json_from(self, url):
        """Runs a get request to a safe session
        
        Arguments:
            url {str} -- URL to be sent get request

        Returns:
            json data from request
        """
        _s = requests.Session()
        logging.debug('Establishing Connection')
        try:
            _req = self.requests_retry_session(session=_s).get(url, headers=self.headers, verify=self.verify)
            _req.raise_for_status()
        except Exception as _x:
            logging.exception('Connection failed: %s', (_x))
        else:
            logging.debug('Connection Successful: %s', (_req.status_code))
            return _req.json()
