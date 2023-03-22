#! /usr/bin/env python
"""
Created on Wed Mar 16 08:28 2023

@author: rjjt
"""

import sys
import os
import argparse
import pandas as pd

from Part import *
import PartDB

import dotenv

dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")

ITEM = 'Item'
QUANTITY = 'Quantity'
REFERENCE = 'Reference'
PART = 'Part'
ASSEMBLY = 'Assembly'
PCB_FOOTPRINT = 'PCB Footprint'
CEPHA_PN = 'Cepha PN'
MFR = 'MFR'
MPN = 'MPN'
MFR2 = 'MFR2'
MPN2 = 'MPN2'


def importBOM(bom_file, name, version, first_row=0):
  db = PartDB.PartDB(db_url)
  bom = BOM(name=name, version=version)
  db.add(bom)

  if first_row > 0:
    csv = pd.read_excel(bom_file, skiprows=first_row-1)
  else:
    csv = pd.read_excel(bom_file)

  csv = csv.dropna(subset=[ITEM, QUANTITY])
  for i, row in csv.iterrows():
    part = db.get_part_by_cspnold(str(int(row[CEPHA_PN])))
    if part is None:
      print("Part %s not found" % str(int(row[CEPHA_PN])))
      continue
    print("Found part %s" % part.cspnold)
    print("Adding BOM item %s: %s" % (row[ITEM], row[PART]))
    bom_item = BOMItem(
        bom_id=bom.id,
        quantity=int(row[QUANTITY]),
        part_id=part.id,
        reference=row[REFERENCE],
        assembly=row[ASSEMBLY]
    )
    db.add(bom_item)


def main():
  parser = argparse.ArgumentParser(description='Import BOM from CSV file')
  parser.add_argument('bom_file', help='BOM CSV file')
  parser.add_argument('name', help='BOM name')
  parser.add_argument('version', help='BOM version (e.g. x.y.z))')
  parser.add_argument('-f', '--first_row', type=int,
                      default=12, help='First row of BOM data')
  args = parser.parse_args()
  importBOM(args.bom_file, args.name, args.version, args.first_row)


if __name__ == '__main__':
  main()
