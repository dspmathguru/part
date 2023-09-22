#! /usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy import *
from sqlalchemy import create_engine

from Part import *

import os
import dotenv

dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

base = Base()
# We will need this for querying
base.query = db_session.query_property()

