"""Initialize API"""

import logging
from logging.handlers import SMTPHandler

from flask import Flask
from flask.logging import default_handler
from flask_restful import Api

from api.cmx import StepIterator
from api.config import Config
from api.connection import SafeSession
from api.resources import ClientResource, RequestLogResource, CMXResource, TestResource
from api.scheduler import Scheduler
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*", 'methods': 'GET', 'supports_credentials': True}})
api = Api(app)

app.config.from_object(Config)

api.add_resource(ClientResource.CLatest, '/api/v2/client/latest')
api.add_resource(ClientResource.CCount, '/api/v2/client/count')
api.add_resource(ClientResource.CAll, '/api/v2/client/all')
api.add_resource(RequestLogResource.LLatest, '/api/v2/log/latest')
api.add_resource(RequestLogResource.LCount, '/api/v2/log/count')
api.add_resource(RequestLogResource.LAll, '/api/v2/log/all')
api.add_resource(CMXResource.pull, '/api/v2/cmx/pull')
#api.add_resource(TestResource.cmx.client_count, '/api/v2/test/cmx/count')

conn = SafeSession(Config.WEB['UID'], 
                   Config.WEB['PWD'], 
                   Config.WEB['VERIFICATION'],
                   Config.CONNECTION['MAX_RETRIES'], 
                   Config.CONNECTION['BACKOFF_FACTOR'], 
                   Config.CONNECTION['STATUS_FORCELIST'])

stepper = StepIterator(Config.API['BASE_RANGE_STEP'])

sched = Scheduler(stepper.base_iterate, Config.SCHEDULER_DELAY_TIME)

if(Config.LOGGING):
    smtp_handler = SMTPHandler(
        mailhost=Config.ERR['MAIL_HOST'],
        fromaddr=Config.ERR['FROM_ADDR'],
        toaddrs=Config.ERR['TO_ADDRS'],
        subject=Config.ERR['SUBJECT_DEFAULT'])
    smtp_handler.setLevel(logging.ERROR)

    for logger in (
        logging.getLogger(),
        logging.getLogger('flask_cors'),
        logging.getLogger('click'),
    ):
        logger.level = logging.DEBUG if Config.DEBUG else logging.ERROR
        logger.addHandler(default_handler)
        logger.addHandler(smtp_handler)