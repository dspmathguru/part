#! /usr/bin/env python

from dotenv import load_dotenv
import os

load_dotenv()

db_key = os.getenv("DATABASE_URI")


print(db_key)
