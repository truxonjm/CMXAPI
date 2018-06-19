"""Interface to PastPortGPS, the web-based Client services for the barge

Returns:
    {Response} - Connection to the CMX API
"""

import logging
import time
from base64 import b64encode
from logging.handlers import SMTPHandler

import requests
from bs4 import BeautifulSoup
from flask.logging import default_handler
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.config import Config

CONN=Config.CONNECTION
ERR=Config.ERR

Retry.BACKOFF_MAX = CONN['BACKOFF_MAX']

smtp_handler = SMTPHandler(
    mailhost=ERR['MAIL_HOST'],
    fromaddr=ERR['FROM_ADDR'],
    toaddrs=ERR['TO_ADDRS'],
    subject=ERR['SUBJECT_DEFAULT'])
smtp_handler.setLevel(logging.ERROR)

LOGGER = logging.getLogger('smtp')
LOGGER.addHandler(smtp_handler)

DEBUGGER = logging.getLogger('debug')

def requests_retry_session(session=None):
    session = session or requests.Session()
    __max = CONN['MAX_RETRIES']
    retry = Retry(
        total=__max,
        read=__max,
        connect=__max,
        backoff_factor=CONN['BACKOFF_FACTOR'],
        status_forcelist=CONN['STATUS_FORCELIST'],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def safe_session(url, uid, pwd):
    s = requests.Session()
    userPassString = "{}:{}".format(uid,pwd)
    usernamePassword = b64encode(userPassString.encode()).decode("ascii")
    headers = {
        'Authorization' : 'Basic %s' % usernamePassword,
        'Cache-Control': "no-cache",
        'Postman-Token': "e4cca5bc-11fb-493f-a169-c82d31b78c5b"
        }
    
    req = requests_retry_session(session=s).get(url, headers=headers, verify=False)
    return req
