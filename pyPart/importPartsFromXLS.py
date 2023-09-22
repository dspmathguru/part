#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 19:17 2023

@author: rjjt
"""

import sys
import os
import argparse
import pandas as pd
from Part import *
import PartDB

import platform
import dotenv

dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(os.getenv("PARTS_XLS"))
parts_xls = os.path.expanduser(os.getenv("PARTS_XLS"))
part_types_csv = os.path.expanduser(os.getenv("PART_TYPES_CSV"))

PN = 'CEPHA P/N'
ITEM = 'Item'
DESCRIPTION = 'DESCRIPTION'
FOOTPRINT = 'FOOTPRINT'
MFR1 = 'Manufacturer 1'
MFR1PN = 'MFR 1 Part Number'
MFR2 = 'Manufacturer 2'
MFR2PN = 'MFR 2 Part Number'

db = PartDB.PartDB(db_url)

def importCompanyTypes():
  # pre seed company types
  ctypes = [
      'manufacturer',
      'distributor',
      'customer'
  ]

  for c in ctypes:
    ctype = CompanyType(name=c)
    db.add(ctype)

def importPartTypes(df):
  for i, row in df.iterrows():
    print("Importing part type %s: %s" % (row['type'], row['prefix']))
    part_type = PartType(type=row['type'], prefix=row['prefix'])
    db.add(part_type)

def importMfr(mfrs):
  mfr_type = db.get_company_type_by_name('manufacturer')
  for mfr in mfrs:
    print("Importing manufacturer %s" % mfr)
    db.add(Company(name=mfr, company_type_id=mfr_type.id, company_type=mfr_type))

def importFootprint(footprints):
  for footprint in footprints:
    print("Importing footprint %s" % footprint)
    db.add(Footprint(name=footprint))

def findPartType(pn, pt_df):
  pns = str(int(pn))
  for i, row in pt_df.iterrows():
    if pd.isna(row['old 1']):
      o1 = 'xxxxxxxxxxxx'
    else:
      o1 = str(int(row['old 1']))
    if pd.isna(row['old 2']):
      o2 = 'xxxxxxxxxxxx'
    else:
      o2 = str(int(row['old 2']))
    if pd.isna(row['old 3']):
      o3 = 'xxxxxxxxxxxx'
    else:
      o3 = str(int(row['old 3']))
    if pd.isna(row['old 4']):
      o4 = 'xxxxxxxxxxxx'
    else:
      o4 = str(int(row['old 4']))
    if pd.isna(row['old 5']):
      o5 = 'xxxxxxxxxxxx'
    else:
      o5 = str(int(row['old 5']))
    if pd.isna(row['old 6']):
      o6 = 'xxxxxxxxxxxx'
    else:
      o6 = str(int(row['old 6']))
    if pns.startswith(o1) or pns.startswith(o2) or pns.startswith(o3) or pns.startswith(o4) or pns.startswith(o5) or pns.startswith(o6):
      return (db.get_part_type_by_type(row['type']), row['prefix'])
  print("Unknown part type for %s" % pns)
  sys.exit(1)


pn_index = {}

def createPartNumber(prefix):
  if prefix in pn_index.keys():
    pn_index[prefix] += 1
    return "%s%06d" % (prefix, pn_index[prefix])
  else:
    pn_index[prefix] = 1
    return "%s%06d" % (prefix, pn_index[prefix])

def importParts(df, pt_df):
  for i, row in df.iterrows():
    print("Importing part %d - %s" % (int(row[PN]), row[DESCRIPTION]))
    part_type, prefix = findPartType(row[PN], pt_df)
    pn = createPartNumber(prefix)
    part = Part(cspn=pn, cspnold=str(
        int(row[PN])), parttype_id=part_type.id, parttype=part_type, description=row[DESCRIPTION])
    db.add(part)
    if not pd.isna(row[MFR1]):
      mfr = db.get_company_by_name(row[MFR1])
      mfr_part = ManufacturerPart(
          company_id=mfr.id,
          company=mfr,
          pn=str(row[MFR1PN]),
          part_id=part.id,
          description=row[DESCRIPTION],
      )
      db.add(mfr_part)
    if not pd.isna(row[MFR2]):
      mfr = db.get_company_by_name(row[MFR2])
      mfr_part = ManufacturerPart(
          company_id=mfr.id,
          company=mfr,
          pn=str(row[MFR2PN]),
          part_id=part.id,
          description=row[DESCRIPTION],
      )
      db.add(mfr_part)


def importPartsFromXLS():
  print("Importing parts from %s" % parts_xls)
  df = pd.read_excel(parts_xls, sheet_name='Master Parts List')
  df = df.dropna(subset=[ITEM, PN])
  df = df[[ITEM, PN, DESCRIPTION, FOOTPRINT, MFR1, MFR1PN, MFR2, MFR2PN]]
  dfPT = pd.read_csv(part_types_csv)

  importCompanyTypes()
  mfrs1 = df[MFR1]
  mfrs = pd.concat([mfrs1, df[MFR2]]).dropna().unique()
  importMfr(mfrs)
  footprints = df[FOOTPRINT].dropna().unique()
  importFootprint(footprints)
  importPartTypes(dfPT)
  importParts(df, dfPT)

def main():
  parser = argparse.ArgumentParser(description='Import parts from XLS')
  parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
  args = parser.parse_args()

  if args.verbose:
    print("Verbose output enabled")

  importPartsFromXLS()


if __name__ == '__main__':
  main()
