"""API Database Resources"""


import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from .logger import time_execution

class SafeSession():
    """Provides a limited scope for transactions and helps security and error handling."""

    #connection = engine.connect()
    #trans = connection.begin()

    # The connection and transaction process would require a painful process of declaring the explicit declaration of 
    # a bare SQL statement for each item to be stored. That's not a fun process to go through.
    

    def __init__(self, db_uri):
        self.engine = create_engine(db_uri, pool_size=20, max_overflow=50)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=self.engine))
        self.base = declarative_base(bind=self.engine)

    @time_execution
    def store(self, obj, show_debug=False):
        """Stores a single object to the database"""
        if show_debug:
            logging.debug('Storing single object')
        try:
            self.session.add(obj)
            self.session.commit()
            if show_debug:
                logging.debug('Storage successful')
        except Exception as _x:
            self.session.rollback()
            logging.exception('Storage failed: %s', (_x))
        finally:
            return obj

    @time_execution
    def store_list(self, obj_list):
        """Stores a list of objects to the database"""
        logging.debug('Beginning list storage')
        try:
            [self.session.add(obj) for obj in obj_list]
            self.session.commit()
            logging.debug('Storage successful')
        except Exception as _x:
            self.session.rollback()
            logging.exception('Storage failed: %s', (_x))
        finally:
            return obj_list
