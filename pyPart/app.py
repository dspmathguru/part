#! /usr/bin/env python

from flask import Flask
from flask_graphql import GraphQLView
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy import create_engine

from Schema import schema
from Part import Base

import os
import dotenv

dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.query = db_session.query_property()

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
  db_session.remove()


if __name__ == '__main__':
  app.run()
