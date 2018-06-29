"""API Database Resources"""


import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from api.logger import time_execution
from api.config import Config

engine = create_engine(Config.DB['URI'])
session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))
base = declarative_base(bind=engine)

@time_execution
def store_list(obj_list):
    """Store the list of objects into the database
    
    Arguments:
        obj_list {Declarative_Base} -- SqlAlchemy Base ORM Type
    
    Returns:
        Declarative_base list -- ORM Objects Stored in database
    """

    [session.add(obj) for obj in obj_list]
    session.commit()
    logging.debug('Stored to database')
    return obj_list

@time_execution
def store(obj):
    """Store an object into the database
    
    Arguments:
        obj {Declarative_Base} -- SqlAlchemy Base ORM Type
    
    Returns:
        Declarative_base -- ORM Object Stored in database
    """

    session.add(obj)
    session.commit()
    logging.debug('Stored to database')
    return obj