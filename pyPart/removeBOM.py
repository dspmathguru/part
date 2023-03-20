#! /usr/bin/env python

import sys
import os
import argparse

from Part import *
import PartDB

import dotenv

dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")

def removeBOM(name, version):
  db = PartDB.PartDB(db_url)
  bom = db.get_bom_by_name_version(name, version)
  if bom is None:
    print("BOM %s %s not found" % (name, version))
    return
  print("Found BOM %s %s" % (bom.name, bom.version))

  for item in bom.items:
    print("Deleting BOM item %s" % item.id)
    db.delete(item)

  print("Deleting BOM %s %s" % (bom.name, bom.version))
  db.delete(bom)

def main():
  parser = argparse.ArgumentParser(description='Delete BOM from database')
  parser.add_argument('name', help='BOM name')
  parser.add_argument('version', help='BOM version')
  args = parser.parse_args()

  removeBOM(args.name, args.version)


if __name__ == '__main__':
  main()
