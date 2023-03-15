#! /usr/bin/env python

from dotenv import load_dotenv
import os

import PartDB
from Part import *

load_dotenv()

db = PartDB.PartDB(os.getenv("DATABASE_URL"))

# Add a footprint
footprint = Footprint(name="SOT-23-5")
db.add(footprint)

# pre seed company types
ctypes = [ 
  'manufacturer', 
  'distributor',
  'customer'
]

for c in ctypes:
  ctype = CompanyType(name = c)
  db.add(ctype)
  
