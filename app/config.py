"""Opens private config values as class"""

import json
import logging
import sys

import urllib3

if sys.version_info[0] < 3:
    from urllib import quote_plus
else:
    from urllib.parse import quote_plus

urllib3.disable_warnings()

class Config(object):
    with open("./config.json", 'r') as stream:
        __vars = json.load(stream)

    ENV=__vars['ENV']
    DEBUG=__vars['DEBUG']
    TESTING=__vars['TESTING']
    LOGGING=__vars['LOGGING']
    RESTFUL_JSON=__vars['RESTFUL_JSON']
    SCHEDULER_DELAY_TIME=__vars['SCHEDULER_DELAY_TIME']
    WEB=__vars['WEB']
    CONNECTION=WEB['CONNECTION']
    DB= __vars['DB']
    ERR=__vars['ERR']

    __quote = quote_plus('DRIVER='+DB['DRIVER']+
            ';SERVER='+DB['SERVER']+';DATABASE='+DB['DATABASE']+
            ';UID='+DB['UID']+';PWD='+DB['PWD'])
    DB['URI'] = 'mssql+pyodbc:///?odbc_connect=%s' % __quote

    if(LOGGING):
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(levelname)s] %(threadName)s: %(message)s')
        

        
