from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.config import Config
from sqlalchemy.ext.declarative import declarative_base

DB=Config.DB
ENGINE = create_engine(DB['URI'])
SESSION = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=ENGINE))
                                    
BASE = declarative_base(bind=ENGINE)                                      